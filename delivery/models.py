#
#       Delivery API Address Model & Validators
#
#               Tue  1 Mar 21:10:18 2016
#

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from .delivery import SERVICES, STATUSES, get_prices, OFFICE
from .signals import order_purchased
from invoicing.models import Invoice

import easypost

TEST_EP_KEY = 'OJwynagQo2hRGHBnKbAiHg'

# Authenticate EasyPost Instance
easypost.api_key = TEST_EP_KEY


POSTAL_REGEX = "[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ] ?[0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]"


# Address Model


class Address(models.Model):
    user = models.ForeignKey('auth.User', null=True, related_name='addresses')

    # Contact
    name = models.CharField(max_length=50)
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
        return "%s, %s, %s, %s, %s" % \
                (self.street, self.city, self.prov, self.postal, self.country)

    def is_local(self):
        if self.city.upper() == 'TORONTO':
            return True
        else:
            return False


# Parcel Model


class Parcel(models.Model):
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    weight = models.FloatField()

    def __str__(self):
        return '%f" x %f" x %f", %foz' % \
            (self.length, self.width, self.height, self.weight)

    def easypost(self):
        return {
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'weight': self.weight
        }


# Shipment Model


class Shipment(models.Model):
    easypost_id = models.CharField(max_length=200, null=True)
    rate_id = models.CharField(max_length=200, null=True)
    # Purchased Only
    tracking_code = models.CharField(max_length=100, null=True)
    postal_label = models.URLField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True)
    price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return 'Shipment: %s' % (self.id)

    def get_rates(self, pickup, dropoff, parcel):
        try:
            shipment = easypost.Shipment.create(
                from_address = pickup,
                to_address = dropoff,
                parcel= parcel
            )
            if not shipment.rates:
                raise Exception
            self.easypost_id = shipment.id
            return shipment.rates
        except Exception as e:
            print 'EasyPost Rates Issue: %s' % (e)
            return []

    def purchase_label(self, rate):
        try:
            shipment = easypost.Shipment.retrieve(self.easypost_id)
            purchase = shipment.buy(rate={ 'id': rate })
            # Initialize EasyPost Fields
            self.rate_id = rate
            self.tracking_code = purchase.tracking_code
            self.postal_label = purchase.postage_label.label_url
            self.price = float(purchase.selected_rate.rate)
            # Return Instance
            return self
        except Exception as e:
            print 'EasyPost Purchase Issue: %s' % (e)
            print e
            # Return None, Indicating Error
            return None

    def get_price(self):
        try:
            shipment = easypost.Shipment.retrieve(self.easypost_id)
            self.price = shipment.selected_rate.rate
            return self.price
        except Exception as e:
            print e
            return None

    def get_status(self):
        try:
            shipment = easypost.Shipment.retrieve(self.easypost_id)
            self.status = shipment.tracker.status
            return self.status
        except Exception as e:
            print e
            return None


# Order Model


class Order(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True, related_name='orders')
    courier = models.ForeignKey(User, null=True,
                                limit_choices_to={'groups__name': 'Couriers'}, related_name='courier')
    # Core Fields
    pickup = models.ForeignKey(Address, null=True, related_name='start')
    dropoff = models.ForeignKey(Address, null=True, related_name='end')
    parcel = models.ForeignKey(Parcel, null=True)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()
    delivery_time = models.TimeField(null=True)
    comments = models.CharField(max_length=200, blank=True)

    # make local and EP prices
    price = models.FloatField(null=True)
    service = models.CharField(max_length=10, choices=SERVICES, null='BASIC')
    status = models.CharField(max_length=2, choices=STATUSES, default='RE')
    invoice_line = models.CharField(max_length=5000, null=True)
    invoice_id = models.ForeignKey(Invoice, null=True, blank=True)
    shipment = models.OneToOneField(Shipment, blank=True, null=True)

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

    def purchase(self, rate):
        if self.is_local:
            prices = get_prices( self.pickup.__str__(), self.dropoff.__str__() )
            prices = self.get_rates()
            if rate == 'BA':
                self.price = prices[0]['price']
            elif rate == 'EX':
                self.price = prices[1]['price']
            self.service = rate
            self.dispatch_purchase(self)
            return self
        else:
            prices = get_prices( self.pickup.__str__(), OFFICE )
            purchase = self.shipment.purchase_label(rate)
            if purchase is not None:
                purchase.save()
                self.price = purchase.price + prices[0]['price']
                self.dispatch_purchase(self)
                return self
            else:
                return None

    def get_rates(self):
        if self.is_local:
            return get_prices( self.pickup.__str__(), self.dropoff.__str__() )
        else:
            self.shipment = Shipment.objects.create()
            ep_rates = self.shipment.get_rates(
                self.pickup.easypost(),
                self.dropoff.easypost(),
                self.parcel.easypost()
            )
            # Initialize Final Rates Array
            rates = []
            if ep_rates:
                prices = get_prices( self.pickup.__str__(), OFFICE )
                for rate in ep_rates:
                    price = float(rate.rate) + prices[0]['price']
                    rates.append({
                        'id': rate.id,
                        'carrier': rate.carrier,
                        'service': rate.service,
                        'rate': str(price),
                        'days': rate.delivery_days
                    })
                # Save Shipment
                self.shipment.save()
            # Return Final Rates Array
            return rates
