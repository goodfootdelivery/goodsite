#
#   Delivery Module
#
#           Thu 10 Mar 11:46:13 2016
#

import googlemaps

GKEY = 'AIzaSyAF5a1ktypMvsvnMMnoaFGHkmt_9vnWfok'
OFFICE = '720 Bathurst St, Toronto, ON M5S 2R4, CA'
PRICE_VECTOR = [0.0075, 0.005, 0.004]

SERVICES = (
        ('EX', 'Express'),
        ('BA', 'Basic'),
    )

STATUSES = (
        ('RE', 'Recieved'),
        ('AS', 'Assigned'),
        ('TR', 'In Transit'),
        ('DE', 'Delivered'),
        ('PD', 'Paid'),
    )


def get_distance(pickup, dropoff):
    client = googlemaps.Client(key=GKEY)
    dist_mat = client.distance_matrix(pickup, dropoff, mode='transit')

    if not dist_mat['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
        return dist_mat['rows'][0]['elements'][0]['duration']['value']
    else:
        return None

def get_prices(pickup, dropoff):
    prices = []
    seconds = get_distance(pickup, dropoff)
    hours = seconds / 3600.00

    nd_rate = round( hours*20.00, 3 )
    if 8.50 > nd_rate:
        prices.append({'service': 'BA', 'price': 8.50})
    elif 60.00 < nd_rate:
        prices.append({'service': 'BA', 'price': 60.00})
    else:
        prices.append({'service': 'BA', 'price': nd_rate})

    ex_rate = round( hours*25.00, 3 )
    if 15.00 > nd_rate:
        prices.append({'service': 'EX', 'price': 15.00})
    elif 60.00 < nd_rate:
        prices.append({'service': 'EX', 'price': 60.00})
    else:
        prices.append({'service': 'EX', 'price': ex_rate})
    return prices
