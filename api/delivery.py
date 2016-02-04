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


if __name__ == '__main__':
    easypost.api_key = TEST_EP_KEY

    pickup = easypost.Address.create(
        company = 'goodfoot',
        street1 = '720 Bathurst St',
        city = 'Toronto',
        state = 'ON',
        country = 'Canada',
        zip = 'M5S 2R4',
        phone = '519-365-7870'
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

    if not shipment.rates:
        print 'Order Failed'
    else:
        print 'Order Success'
        shipment2 = easypost.Shipment.retrieve(shipment.id)
        for rate in shipment2.rates:
           pass
        print shipment2
