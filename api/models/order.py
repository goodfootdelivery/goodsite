#
#       Delivery API Order Model & Validators
#
#               Tue  1 Mar 21:10:18 2016
#

from django.db import models
from django.contrib.auth.models import User
from api.delivery import SERVICES, STATUSES, get_distance, get_g_prices, TEST_EP_KEY
from .address import Address
from .parcel import Parcel

import easypost
import googlemaps

OFFICE = '720 Bathurst St, Toronto, ON M5S 2R4, CA'
GKEY = 'AIzaSyAF5a1ktypMvsvnMMnoaFGHkmt_9vnWfok'

# Authenticate EasyPost Instance
easypost.api_key = TEST_EP_KEY


### ORDER MODEL ###

class Order(models.Model):
    owner = models.ForeignKey('auth.User', null=True, blank=True, related_name='orders')
    courier = models.ForeignKey(User, null=True,
                                limit_choices_to={'groups__name': 'Couriers'}, related_name='courier')
    # Core Fields
    pickup = models.ForeignKey(Address, null=True, related_name='start')
    dropoff = models.ForeignKey(Address, null=True, related_name='end')
    parcel = models.ForeignKey(Parcel, null=True)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(null=True)
    delivery_time = models.TimeField(null=True)
    comments = models.CharField(max_length=200, blank=True)

    # make local and EP prices
    price = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=STATUSES, default='RE')
    service = models.CharField(max_length=2, choices=SERVICES, default=None)

    # EasyPost ONLY
    easypost_id = models.CharField(max_length=200, blank=True, null=True)
    rate_id = models.CharField(max_length=200, blank=True, null=True)

    # Purchased Only
    tracking_code = models.CharField(max_length=100, null=True, blank=True)
    postal_label = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return "Order: #%s, Date: %s" % (str(self.id), str(self.order_date))

    def is_local(self):
        if self.dropoff.is_local() is True:
            return True
        else:
            return False

    def easypost(self):
        rates = []
        try:
            shipment = easypost.Shipment.create(
                from_address = self.pickup.easypost(),
                to_address = self.dropoff.easypost(),
                parcel= self.parcel.easypost()
            )
            if not shipment.rates:
                raise Exception
            else:
                for rate in shipment.rates:
                    rates.append({
                        'id': rate.id,
                        'carrier': rate.carrier,
                        'service': rate.service,
                        'rate': rate.rate,
                        'days': rate.delivery_days
                    })
            self.easypost_id = shipment.id
        except Exception as e:
            print e
        return rates

    def purchase(self, rate):
        try:
            shipment = easypost.Shipment.retrieve(self.easypost_id)
            purchase = shipment.buy(rate={ 'id': rate })

            # Initialize EasyPost Fields
            self.rate_id = rate
            self.tracking_code = purchase.tracking_code
            self.postal_label = purchase.postage_label.label_url
            return True

        except Exception as e:
            print e
            return False

    def get_prices(self):
        return get_g_prices( self.pickup.__str__(), self.dropoff.__str__() )
