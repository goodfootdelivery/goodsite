from django.db import models
from django.contrib.auth.models import User
from .delivery import SERVICES, STATUSES


class Address(models.Model):
    owner = models.ForeignKey('auth.User', related_name='addresses')
    contact_name = models.CharField(max_length=30, blank=True)
    contact_number = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=100, null=True)
    unit = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    comments = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return '%s' % (self.address)


class Parcel(models.Model):
    length = models.CharField(max_length=200, choices=STATUSES, default='RE')
    width = models.CharField(max_length=200, choices=STATUSES, default='RE')
    height = models.CharField(max_length=200, choices=STATUSES, default='RE')
    weight = models.CharField(max_length=200, choices=STATUSES, default='RE')


class Order(models.Model):
    owner = models.ForeignKey('auth.User', related_name='orders')
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(null=True)
    status = models.CharField(max_length=2, choices=STATUSES, default='RE')
    service = models.CharField(max_length=2, choices=SERVICES, default=None)
    pickup = models.ForeignKey(Address, null=True, related_name='start')
    dropoff = models.ForeignKey(Address, null=True, related_name='end')
    parcel = models.OneToOneField(Parcel, null=True)
    courier = models.ForeignKey(User, null=True,
                        limit_choices_to={'groups__name': 'Couriers'}, related_name='courier')

    def __str__(self):
        return "Order: #%s, Date: %s" % (str(self.id), str(self.order_date))
