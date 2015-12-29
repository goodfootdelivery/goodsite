import googlemaps
import easypost

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
        ('BD', 'Billed'),
    )

PARCELS = (
    ('EV', 'Envelope'),
    ('BX', 'Box'),
    ('BG', 'Bag'),
)

class InvalidAddress(Exception):
    def __init__(self, issue):
        self.issue = issue

    def __str__(self):
        return repr(self.issue)


class InvalidOrder(Exception):
    def __init__(self, issue):
        self.issue = issue

    def __str__(self):
        return repr(self.issue)


#### TESTING ####

tdot = '17 Raglan Ave, Toronto, ON M6C 2K7, Canada'
home = '48 Parkview Court, Chatham, ON N7M 6H9, Canada'
buxx = 'Nonsense'

if __name__ == '__main__':
    pass
