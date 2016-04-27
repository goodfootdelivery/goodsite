from rest_framework.exceptions import APIException
from .models import Order, Address, Parcel, Shipment
from goodfoot.settings import OFFICE_SHORT, OFFICE_LONG, G_KEY, EP_KEY
import googlemaps
import easypost

easypost.api_key = EP_KEY


# Google Services


class GoogleService(object):
    @staticmethod
    def get_distance(pickup, dropoff):
        client = googlemaps.Client(key=G_KEY)
        dist_mat = client.distance_matrix(pickup, dropoff, mode='transit')

        if not dist_mat['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
            return dist_mat['rows'][0]['elements'][0]['duration']['value']
        else:
            raise Exception('Googlemaps Error')

    @staticmethod
    def get_local_rates(pickup, dropoff=OFFICE_SHORT):
        prices = []
        seconds = GoogleService.get_distance(pickup, dropoff)
        long_distance_trigger = 1.2
        hourly_rate = 16.00
        hours = seconds / 3600.00

        nd_rate = round( hours*20.00, 3 )
        if 8.50 > nd_rate:
            prices.append({'service': 'BASIC', 'price': 8.50})
        elif 60.00 < nd_rate:
            prices.append({'service': 'BASIC', 'price': 60.00})
        else:
            prices.append({'service': 'BASIC', 'price': nd_rate})

        ex_rate = round( hours*25.00, 3 )
        if 15.00 > nd_rate:
            prices.append({'service': 'EXPRESS', 'price': 15.00})
        elif 60.00 < nd_rate:
            prices.append({'service': 'EXPRESS', 'price': 60.00})
        else:
            prices.append({'service': 'EXPRESS', 'price': ex_rate})
        return prices



# EasyPost Services



class EasypostService(object):
    # create Easypost Address
    @staticmethod
    def create_address(**kwargs):
        address = easypost.Address.create(
                name = kwargs.get('name'),
                phone = kwargs.get('phone'),
                street1 = kwargs.get('street'),
                street2 = kwargs.get('unit'),
                city = kwargs.get('city'),
                state = kwargs.get('prov'),
                country = kwargs.get('country'),
                zip = kwargs.get('postal'),
        )
        return address.id

    # creates easypost shipment, grabs rates and operates on them
    @staticmethod
    def get_shipment_rates(pickup, dropoff, parcel, local_price):
        shipment = easypost.Shipment.create(
            from_address = OFFICE_LONG,
            to_address = { 'id': dropoff },
            parcel = {
                'length': parcel.get('length'),
                'width': parcel.get('width'),
                'height': parcel.get('height'),
                'weight': parcel.get('weight'),
            }
        )
        if not shipment.rates:
            raise Exception('Invalid Shipment')
        # rate operator function
        def format_rates(rate):
            price = float(rate.rate) + local_price
            return {
                'id': rate.id,
                'carrier': rate.carrier,
                'service': rate.service,
                'rate': str(price),
                'days': rate.delivery_days
            }
        return {
            'easypost_id': shipment.id,
            'rates': map(format_rates, shipment.rates)
    }

    # returns dict of easypost object fields available after purchase
    @staticmethod
    def purchase_label(easypost_id, rate_id):
        shipment = easypost.Shipment.retrieve(easypost_id)
        purchase = shipment.buy(rate={ 'id': rate_id })
        return {
            'tracking_code': purchase.tracking_code,
            'postal_label': purchase.postage_label.label_url,
            'cost': float(purchase.selected_rate.rate)
        }
