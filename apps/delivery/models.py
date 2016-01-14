from django.db import models
from django.contrib.auth.models import User
from .delivery import SERVICES, STATUSES


class Address(models.Model):
    owner = models.ForeignKey('auth.User', related_name='addresses')
    contact_name = models.CharField(max_length=30, blank=True)
    contact_number = models.CharField(max_length=12, blank=True)
    street = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=10, null=True)
    region = models.CharField(max_length=2, null=True)
    country = models.CharField(max_length=2, null=True)
    unit = models.CharField(max_length=20, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    comments = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return '%s, %s' % (self.street, self.region)


class Parcel(models.Model):
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    weight = models.FloatField()

    def __str__(self):
        return '%f" x %f" x %f", %foz' % \
            (self.length, self.width, self.height, self.weight)


class Shipment(models.Model):
    tracking_code = models.CharField(max_length=100, null=True, blank=True)
    postal_label = models.URLField(max_length=200, blank=True, null=True)
    pickup = models.ForeignKey(Address, null=True, related_name='start')
    dropoff = models.ForeignKey(Address, null=True, related_name='end')
    parcel = models.OneToOneField(Parcel, null=True)

    def get_price(self):
        pass


class Order(models.Model):
    owner = models.ForeignKey('auth.User', related_name='orders')
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(null=True)
    price = models.FloatField(blank=True, null=True)
    shipment = models.OneToOneField(Shipment)
    status = models.CharField(max_length=2, choices=STATUSES, default='RE')
    service = models.CharField(max_length=2, choices=SERVICES, default=None)
    courier = models.ForeignKey(User, null=True,
                        limit_choices_to={'groups__name': 'Couriers'}, related_name='courier')

    def __str__(self):
        return "Order: #%s, Date: %s" % (str(self.id), str(self.order_date))
