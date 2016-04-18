from django.core.exceptions import ObjectDoesNotExist
from .models import Client
from .invoice import FB_URL, API_KEY, COMPANY
from refreshbooks import api


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
