#
#       Delivery API Address Model & Validators
#
#               Tue  1 Mar 21:10:18 2016
#

from django.db import models
from django.core.validators import RegexValidator

POSTAL_REGEX = "[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ] ?[0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]"

#
#       Address Model
#
class Address(models.Model):
    owner = models.ForeignKey('auth.User', null=True, related_name='addresses')

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
        if self.city.upper() is 'TORONTO':
            return True
        else:
            return False

