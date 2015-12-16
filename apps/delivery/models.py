from django.db import models
from django.contrib.auth.models import User
# Tue Dec  8 20:45:29 2015"

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
    latitude = models.DecimalField(null=True, max_digits=60, decimal_places=30)
    longitude = models.DecimalField(null=True, max_digits=60, decimal_places=30)
    comments = models.CharField(max_length=200, blank=True)
    saved = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.address)


class Order(models.Model):
    user = models.ForeignKey(User, blank=False, null=True)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUSES, default='RE')
    courier = models.ForeignKey(User,
        limit_choices_to={'groups__name': 'Couriers'}, related_name='courier')
    price = models.DecimalField(null=True, max_digits=5, decimal_places=2)

    def __str__(self):
        return "Order: %s, \tUser: %s, \tDate: %s, \tStatus: %s" \
        % (str(self.id), str(self.user), str(self.date), str(self.status))


class OrderDetails(models.Model):
    order = models.OneToOneField(Order, primary_key=True)
    delivery_date = models.DateField(null=True)
    service = models.CharField(max_length=2, choices=SERVICES, default=None)
    pickup = models.ForeignKey(Address, null=True, related_name='start')
    dropoff = models.ForeignKey(Address, null=True, related_name='end')
    travel_time = models.DurationField(null=True)
