import easypost
import googlemaps

GKEY = 'AIzaSyAF5a1ktypMvsvnMMnoaFGHkmt_9vnWfok'
OFFICE = '720 Bathurst St, Toronto, ON M5S 2R4, CA'
TEST_EP_KEY = 'OJwynagQo2hRGHBnKbAiHg'

easypost.api_key = TEST_EP_KEY

SERVICES = (
        ('BASIC', 'Basic'),
        ('EXPRESS', 'Express'),
    )

STATUSES = (
        ('RE', 'Recieved'),     #
        ('AS', 'Assigned'),     ## Active
        ('TR', 'In Transit'),   #
        ('DE', 'Delivered'),    # Outstanding
        ('PD', 'Paid'),         # Cleared
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


