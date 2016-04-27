#
#       Delivery API Address Model & Validators
#
#               Tue  1 Mar 21:10:18 2016
#

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from .signals import order_purchased
from invoicing.models import Invoice
import datetime


POSTAL_REGEX = "[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ] ?[0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]"


class Place(models.Model):
    google_id = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=200, null=True)
    comments = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return 'Address Instructions:\n\t%s' % (self.comments)



# Address Model


class Address(models.Model):
    BOOK = (
            ('PI', 'Pickup'),
            ('DR', 'Dropoff'),
    )
    user = models.ForeignKey('auth.User', null=True, related_name='addresses')
    place = models.ForeignKey(Place, null=True, blank=True)
    saved = models.CharField(max_length=10, null=True, choices=BOOK, default='PI')
    # Contact
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True)
    # Address
    street = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=50)
    prov = models.CharField(max_length=20)
    postal = models.CharField(max_length=10, validators=[RegexValidator(regex=POSTAL_REGEX)])
    country = models.CharField(max_length=2, default='CA')
    # Coordinates
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    # Easypost
    easypost_id = models.CharField(max_length=200, null=True)

    def easypost(self):
        return {
            'name': self.name,
            'phone': self.phone or None,
            'street1': self.street,
            'street2': self.unit or None,
            'city': self.city,
            'state': self.prov,
            'country': self.country,
            'zip': self.postal,
        }

    def __str__(self):
        return "%s, %s, %s %s, %s" % \
                (self.street, self.city, self.prov, self.postal, self.country)

    def is_local(self):
        if self.city.upper() == 'TORONTO':
            return True
        else:
            return False


# Parcel Model


class Parcel(models.Model):
    # Dimensions
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    weight = models.FloatField()
    # Easypost
    easypost_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return '%f" x %f" x %f", %foz' % \
            (self.length, self.width, self.height, self.weight)


# Order Model


class Order(models.Model):
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
    user = models.ForeignKey('auth.User', null=True, blank=True, related_name='user')
    courier = models.ForeignKey(User, null=True,
                                limit_choices_to={'groups__name': 'Couriers'}, related_name='courier')
    # Core Fields
    pickup = models.ForeignKey(Address, null=True, related_name='start')
    dropoff = models.ForeignKey(Address, null=True, related_name='end')
    parcel = models.ForeignKey(Parcel, null=True)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()
    ready_time_start = models.TimeField()
    ready_time_end = models.TimeField(default=datetime.time(18,00))
    comments = models.CharField(max_length=200, blank=True)
    price = models.FloatField(null=True)
    service = models.CharField(max_length=10, choices=SERVICES, default='BASIC')
    status = models.CharField(max_length=2, choices=STATUSES, default='RE')
    invoice_line = models.CharField(max_length=5000, null=True)
    invoice_id = models.ForeignKey(Invoice, null=True, blank=True)
    # Extra Field For Serialization Purposes
    rates = []

    def __str__(self):
        return "Order: #%s, Date: %s" % (str(self.id), str(self.order_date))

    @property
    def is_local(self):
        if self.dropoff.is_local():
            return True
        else:
            return False

    def dispatch_purchase(self, instance):
        order_purchased.send(sender=self.__class__, order=instance)



# Shipment Model


class Shipment(models.Model):
    order = models.OneToOneField(Order, blank=True, null=True)
    easypost_id = models.CharField(max_length=200)
    # Purchased Only
    rate_id = models.CharField(max_length=200, null=True)
    cost = models.FloatField(blank=True, null=True)
    tracking_code = models.CharField(max_length=100, null=True)
    postal_label = models.URLField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True)

    def __str__(self):
        return 'Shipment: %s' % (self.id)

