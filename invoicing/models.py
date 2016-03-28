from django.db import models
from delivery.models import Address, Order

from .invoice import FB_URL, API_KEY, COMPANY
from refreshbooks import api


STATUSES = (
        ('CR', 'Created'),
        ('SE', 'Sent'),
        ('PA', 'Paid'),
    )

# Freshbooks Client information

class Client(models.Model):
    user = models.OneToOneField('auth.User', unique=True)
    freshbooks_id = models.CharField(max_length=10000)
    email = models.EmailField(max_length=30)
    # Client Invoice Optional Fields
    first_name = models.CharField(max_length=10000)
    last_name = models.CharField(max_length=10000)
    organization = models.CharField(max_length=10000)
    phone = models.CharField(max_length=10000)

    def register(self, user):
        try:
            fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
            client = fb.client.create(
                client={
                    'email': user.email,
                    'username': user.username,
                    'password': user.password
                }
            )
            self.user = user
            self.email = user.email
            self.freshbooks_id =  client.client_id
        except Exception as e:
            print e

    def new_invoice(self):
        fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
        response = fb.invoice.create(
            invoice=dict(
                client_id= self.freshbooks_id,
            )
        )


# Freshbooks Invoice information

class Invoice(models.Model):
    client = models.ForeignKey(Client)
    freshbooks_id = models.CharField(max_length=10000)
    sent_date = models.DateField()
    status = models.CharField(max_length=2, choices=STATUSES, default='CR')

    def add_line(self, order):
        # Update Invoice Via Api
        pass

    def send_bill(self):
        pass
