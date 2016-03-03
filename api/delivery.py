import googlemaps
import easypost

OFFICE = '720 Bathurst St, Toronto, ON M5S 2R4, CA'

TEST_EP_KEY = 'OJwynagQo2hRGHBnKbAiHg'
SECRET_EP_KEY = 'NhPygTn6jeiwKLPW5GLhug'

GKEY = 'AIzaSyAF5a1ktypMvsvnMMnoaFGHkmt_9vnWfok'
PRICE_VECTOR = [0.0075, 0.005, 0.004]

SERVICES = (
        ('EX', 'Express'),
        ('SD', 'Same Day'),
        ('ND', 'Next Day'),
    )

STATUSES = (
        ('RE', 'Recieved'),
        ('AS', 'Assigned'),
        ('TR', 'In Transit'),
        ('DE', 'Delivered'),
        ('PD', 'Paid'),
    )

# def validate(self, data):
#     pickup = data.get('pickup')
#     dropoff = data.get('dropoff')
#     client = googlemaps.Client(key=GKEY)
#     if not dropoff.city == 'Toronto':
#         destination = OFFICE
#     else:
#         destination = dropoff.__str__()
#     trip = client.distance_matrix(
#         pickup.__str__(),
#         destination,
#         mode = 'transit'
#     )
#     if not trip['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
#         return data
#     else:
#         raise serializers.ValidationError(
#             'Please Ensure both addresses are valid and try again'
#         )

def get_distance(pickup, dropoff):
    client = googlemaps.Client(key=GKEY)
    dist_mat = client.distance_matrix(pickup, dropoff, mode='transit')

    if not dist_mat['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
        return dist_mat['rows'][0]['elements'][0]['duration']['value']
    else:
        return None

def get_g_prices(pickup, dropoff):
    rates = []
    seconds = get_distance(pickup, dropoff)
    hours = seconds % 3600

    nd_rate = hours*20.00
    if 8.50 > nd_rate:
        rates.append({'service': 'ND', 'price': 8.50})
    elif 60.00 < nd_rate:
        rates.append({'service': 'ND', 'price': 60.00})
    else:
        rates.append({'service': 'ND', 'price': nd_rate})

    ex_rate = hours*25.00
    if 15.00 > nd_rate:
        rates.append({'service': 'EX', 'price': 15.00})
    elif 60.00 < nd_rate:
        rates.append({'service': 'EX', 'price': 60.00})
    else:
        rates.append({'service': 'EX', 'price': ex_rate})

    return rates

### TESTING ###
if __name__ == '__main__':
    easypost.api_key = TEST_EP_KEY

    # pickup = easypost.Address.create(
    #     company = 'goodfoot',
    #     # street1 = '720 Bathurst St',
    #     city = 'Toronto',
    #     state = 'ON',
    #     country = 'Canada',
    #     zip = 'M5S 2R4',
    #     phone = '519-365-7870'
    # )


    try:
        pickup = easypost.Address.create(
            street1 = '720 Bathurst St',
            city = 'Toronto',
            state = 'ON',
            country = 'CA',
            # zip = 'M5S 2R4'
        )

        dropoff = easypost.Address.create(
            company = 'connor',
            street1 = '17 Raglan Ave',
            street2 = 'Unit 15',
            city = 'Toronto',
            state = 'ON',
            country = 'CA',
            zip = 'M6C 2K7',
            phone = '519-351-0361'
        )

        parcel = easypost.Parcel.create(
            length = 9.5,
            width = 9.5,
            height = 9.5,
            weight = 9.5,
        )
        shipment = easypost.Shipment.create(
            to_address = dropoff,
            from_address = pickup,
            parcel = parcel
        )
        print shipment
    except Exception as e:
        print e

    if not shipment.rates:
        print 'Order Failed'
    else:
        print 'Order Success'
        shipment2 = easypost.Shipment.retrieve(shipment.id)
        for rate in shipment2.rates:
            print rate
