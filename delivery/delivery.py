import googlemaps
import easypost

TEST_EP_KEY = 'yARJbUTstAI0WNeVQLxK4g'
SECRET_EP_KEY = None

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


### TESTING ###
if __name__ == '__main__':
    tdot = '17 Raglan Ave, Toronto, ON M6C 2K7, Canada'
    home = '48 Parkview Crt, Chatham, ON N7M 6H9, Canada'
    buxx = 'Nonsense'


    x = 29
    y = {'here': x}
    x += 23
    print x
    # y = {'here': x}
    print y['here']

