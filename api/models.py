from django.db import models
from django.contrib.auth.models import User
from .delivery import SERVICES, STATUSES, get_distance


class Address(models.Model):
    owner = models.ForeignKey('auth.User', null=True, blank=True, related_name='addresses')
    # Contact
    name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    # Address
    street = models.CharField(max_length=100, null=True)
    postal = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=50, null=True)
    prov = models.CharField(max_length=2, null=True)
    country = models.CharField(max_length=2, null=True)
    unit = models.CharField(max_length=20, blank=True)
    # Extra Info
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    comments = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return '%s, %s' % (self.street, self.prov)

    @property
    def easypost(self):
        return {
            'name': self.name or None,
            'phone': self.phone or None,
            'street1': self.street,
            'street2': self.unit or None,
            'city': self.city,
            'state': self.prov,
            'country': self.country,
            'zip': self.postal,
        }

    def formatted(self):
        return self.street + ', ' + self.city + ', ' \
            + self.prov + ' ' + self.postal + ', ' \
            + self.country


class Parcel(models.Model):
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    weight = models.FloatField()

    def __str__(self):
        return '%f" x %f" x %f", %foz' % \
            (self.length, self.width, self.height, self.weight)


class Order(models.Model):
    owner = models.ForeignKey('auth.User', null=True, blank=True, related_name='orders')
    courier = models.ForeignKey(User, null=True,
                                limit_choices_to={'groups__name': 'Couriers'}, related_name='courier')

    # CORE FIELDS
    pickup = models.ForeignKey(Address, null=True, related_name='start')
    dropoff = models.ForeignKey(Address, null=True, related_name='end')
    parcel = models.ForeignKey(Parcel, null=True)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(null=True)
    delivery_time = models.TimeField(null=True)
    local = models.BooleanField(default=True)
    # make local and EP prices
    price = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=STATUSES, default='RE')
    service = models.CharField(max_length=2, choices=SERVICES, default=None)

    # EASYPOST ONLY
    shipping_id = models.CharField(max_length=200, blank=True, null=True)
    rate_id = models.CharField(max_length=200, blank=True, null=True)
    postal_label = models.URLField(max_length=200, blank=True, null=True)
    tracking_code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "Order: #%s, Date: %s" % (str(self.id), str(self.order_date))

    def get_prices(self):
        rates = []
        seconds = get_distance(self.pickup.formatted(), self.dropoff.formatted())
        hours = seconds % 3600

        nd_rate = hours*20.00
        if 8.50 > nd_rate:
            rates.append({'service': 'ND', 'price': 8.50})
        elif 60.00 < nd_rate:
            rates.append({'service': 'ND', 'price': 60.00})
        else:
            rates.append({'service': 'ND', 'price': nd_rate})

        ex_rate = hours*25.00
        if 15.00 > nd_rate:
            rates.append({'service': 'EX', 'price': 15.00})
        elif 60.00 < nd_rate:
            rates.append({'service': 'EX', 'price': 60.00})
        else:
            rates.append({'service': 'EX', 'price': ex_rate})

        return rates
