from django.db import models
from delivery.models import Address

import refreshbooks


# Freshbooks Client information

class Client(models.Model):
    user = models.OneToOneField('auth.User', unique=True)
    freshbooks_id = models.CharField(max_length=10000)
    address = models.OneToOneField(Address)


# Freshbooks Invoice information

class Invoice(models.Model):
    client = models.ForeignKey(Client)
    freshbooks_id = models.CharField(max_length=10000)
