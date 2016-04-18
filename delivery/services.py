from rest_framework.exceptions import APIException
from .models import Order, Address, Parcel, Shipment
import googlemaps
import easypost

GKEY = 'AIzaSyAF5a1ktypMvsvnMMnoaFGHkmt_9vnWfok'
TEST_EP_KEY = 'OJwynagQo2hRGHBnKbAiHg'

easypost.api_key = TEST_EP_KEY

OFFICE_SHORT = '720 Bathurst St, Toronto, ON M5S 2R4, CA'
OFFICE_LONG = {
    'name' : 'GoodFoot Delivery Office',
    'phone' : '416 572 3771',
    'street1' : '720 Bathurst St',
    'street2' : '411',
    'city' : 'Toronto',
    'state' : 'ON',
    'country' : 'Canada',
    'zip' : 'M5S 2R4'
}


# Google Services


# Accepts Two Strings
def get_distance(pickup, dropoff):
    client = googlemaps.Client(key=GKEY)
    dist_mat = client.distance_matrix(pickup, dropoff, mode='transit')

    if not dist_mat['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
        return dist_mat['rows'][0]['elements'][0]['duration']['value']
    else:
        raise Exception('Googlemaps Error')


def get_local_rates(pickup, dropoff=OFFICE_SHORT):
    prices = []
    seconds = get_distance(pickup, dropoff)
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


# create Easypost Address
# Accepts a Dict of Strs
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
def purchase_label(easypost_id, rate_id):
    shipment = easypost.Shipment.retrieve(easypost_id)
    purchase = shipment.buy(rate={ 'id': rate_id })
    return {
        'tracking_code': purchase.tracking_code,
        'postal_label': purchase.postage_label.label_url,
        'cost': float(purchase.selected_rate.rate)
    }
