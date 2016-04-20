from django.core.exceptions import ObjectDoesNotExist
from .models import Client
from refreshbooks import api

# Production
# COMPANY = 'Good Foot Support Services (Good Foot Delivery)'
# FB_URL = 'goodfootdelivery.freshbooks.com'
# API_KEY = '1dc85e1ad7a0ac4a9840e4687e94ac20'

# Testing
COMPANY = 'Goodfoot Delivery Gamma'
FB_URL = 'goodfootdeliverygamma.freshbooks.com'
API_KEY = '0e7d9e834a671c665ada820250babc01'


class FreshbooksService(object):
    # Create a New Client
    @staticmethod
    def create_client(user):
        try:
            fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
            client = fb.client.create(
                client={
                    'email': user.email,
                    'username': user.username,
                    'password': user.password
                }
            )
        except Exception as e:
            print 'Freshbook Client Registration Error: %s' % (e)
            return None
        else:
            return client.client_id

    # Update Client Info.
    @staticmethod
    def update_client(**kwargs):
        pass

    # Create a New Freshbooks Invoice
    @staticmethod
    def create_invoice(user):
        try:
            client = Client.objects.get(user=user)
            fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
            resp = fb.invoice.create(
                invoice=dict(
                    client_id= client.freshbooks_id,
                )
            )
        except ObjectDoesNotExist as e:
            print 'Invoice Creation Error %s' % (e)
            return None
        except Exception as e:
            print 'Invoice Creation Error %s' % (e)
            return None
        else:
            return resp.invoice_id
    # Return Invoice Total
    @staticmethod
    def get_invoice_amount(invoice_id):
        try:
            fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
            resp = fb.invoice.get(invoice_id=invoice_id)
        except Exception:
            return None
        else:
            return resp.invoice.amount
