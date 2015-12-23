from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

import googlemaps

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


class Address(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    contact_name = models.CharField(max_length=30, blank=True)
    contact_number = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=100, null=True)
    unit = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    comments = models.CharField(max_length=200, blank=True)
    saved = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.address)

    @property
    def make_point(self):
        crds = self.location.split(',')
        return [float(x) for x in crds]

    @property
    def get_address(self):
        addr = self.address.split(',')
        return [x.strip() for x in addr]


class Order(models.Model):
    user = models.ForeignKey(User, blank=False, null=True)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(null=True)
    status = models.CharField(max_length=2, choices=STATUSES, default='RE')
    service = models.CharField(max_length=2, choices=SERVICES, default=None)
    pickup = models.ForeignKey(Address, null=True, related_name='start')
    dropoff = models.ForeignKey(Address, null=True, related_name='end')
    dist_mat = JSONField()
    courier = models.ForeignKey(User, null = True,
        limit_choices_to={'groups__name': 'Couriers'}, related_name='courier')

    def __str__(self):
        return "Order: #%s, Date: %s" % (str(self.id), str(self.order_date))

    @property
    def get_duration(self):
        return self.dist_mat['rows'][0]['elements'][0]['duration']['text']

    @property
    def get_prices(self):
        points = self.dist_mat['rows'][0]['elements'][0]['duration']['value']
        return [float(points)*x for x in PRICE_VECTOR]

    def set_dist_mat(self):
        client = googlemaps.Client(key=GKEY)
        self.dist_mat = client.distance_matrix(self.pickup.address, self.dropoff.address, mode='transit')
        print self.dist_mat

    def save(self, *args, **kwargs):
        self.set_dist_mat()
        super(Order, self).save(*args, **kwargs)

