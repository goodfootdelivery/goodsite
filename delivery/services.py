from restframework.exceptions import APIException
from .models import Order, Address, Parcel, Shipment
import easypost
import googlemaps

GKEY = 'AIzaSyAF5a1ktypMvsvnMMnoaFGHkmt_9vnWfok'
OFFICE = '720 Bathurst St, Toronto, ON M5S 2R4, CA'
TEST_EP_KEY = 'OJwynagQo2hRGHBnKbAiHg'

easypost.api_key = TEST_EP_KEY

# Raising Assertion Errors If Service Functions are the Wrong Type
def accepts(*types):
    def check_accepts(f):
        assert len(types) == f.func_code.co_argcount
        def new_f(*args, **kwds):
            for (a, t) in zip(args, types):
                assert isinstance(a, t), \
                       "arg %r does not match %s" % (a,t)
            return f(*args, **kwds)
        new_f.func_name = f.func_name
        return new_f
    return check_accepts


# Google Services


@accepts(str, str)
def get_distance(pickup, dropoff):
    client = googlemaps.Client(key=GKEY)
    dist_mat = client.distance_matrix(pickup, dropoff, mode='transit')

    if not dist_mat['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
        return dist_mat['rows'][0]['elements'][0]['duration']['value']
    else:
        return None


@accepts(str, str)
def get_prices(pickup, dropoff=OFFICE):
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


@accepts(str, str, dict)
def get_non_local_rates(pickup, dropoff, parcel):
    shipment = easypost.Shipment.create(from_address=pickup, to_address=dropoff, parcel=parcel)
    if not shipment.rates:
        raise Exception('Invalid Shipment')
    prices = get_prices(pickup.__str__(), OFFICE)
    # Polish Rate Function
    def format_rates(rate):
        price = float(rate.rate) + prices[0]['price']
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


# returns dict of
@accepts(str, str)
def purchase_label(easypost_id, rate_id):
    shipment = easypost.Shipment.retrieve(self.easypost_id)
    purchase = shipment.buy(rate={ 'id': rate_id })
    return {
        'tracking_code': purchase.tracking_code,
        'postal_label': purchase.postage_label.label_url,
        'price': float(purchase.selected_rate.rate)
    }
