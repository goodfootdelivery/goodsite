from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

from .delivery import PRICE_VECTOR, SERVICES, STATUSES

import googlemaps
GKEY = 'AIzaSyAF5a1ktypMvsvnMMnoaFGHkmt_9vnWfok'


class Address(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    contact_name = models.CharField(max_length=30, blank=True)
    contact_number = models.CharField(max_length=12, blank=True)
    # Geocompleted Fields
    formatted = models.CharField(max_length=100, null=True)
    number = models.CharField(max_length=100, null=True)
    street = models.CharField(max_length=100, null=True)
    locality = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=10, null=True)
    region = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    # End Geocompleted Fields
    unit = models.CharField(max_length=20, blank=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    saved = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.address)

    @property
    def make_point(self):
        crds = self.location.split(',')
        return [float(x) for x in crds]

    @property
    def get_address(self):
        addr = self.formatted.split(',')
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
    courier = models.ForeignKey(User,
        limit_choices_to={'groups__name': 'Couriers'}, related_name='courier')

    def __str__(self):
        return "Order: #%s, Date: %s" % (str(self.id), str(self.order_date))

    @property
    def duration(self):
        if self.dist_mat:
            return self.dist_mat['rows'][0]['elements'][0]['duration']['text']

    @property
    def prices(self):
        points = self.dist_mat['rows'][0]['elements'][0]['duration']['value']
        return [float(points)*x for x in PRICE_VECTOR]

    def set_dist_mat(self):
        client = googlemaps.Client(key=GKEY)
        dist_mat = client.distance_matrix(self.pickup.formatted, self.dropoff.formatted, mode='transit')
        print self.dist_mat

        if not dist_mat['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
            self.dist_mat = dist_mat
        else:
            self.dist_mat = None

    # def check(self):
    #     try:
    #         self.pickup.check()
    #     except InvalidAddress as e:
    #         message = '%s in Pickup Address' % e
    #         raise InvalidOrder(message)

    #     try:
    #         self.dropoff.check()
    #     except InvalidAddress as e:
    #         message = '%s in Dropoff Address' % e
    #         raise InvalidOrder(message)

    #     if self.dist_mat is None:
    #         raise InvalidOrder('No Transit Route Found')

    def save(self, *args, **kwargs):
        self.set_dist_mat()
        super(Order, self).save(*args, **kwargs)


class Parcel(models.Model):
    length = models.FloatField(null=True)
    width = models.FloatField(null=True)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    local = models.BooleanField(default=False)
