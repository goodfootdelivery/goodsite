from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from .invoice import FB_URL, API_KEY, COMPANY
from refreshbooks import api


STATUSES = (
        ('CR', 'Created'),
        ('BL', 'Billable'),
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

    @classmethod
    def register(cls, user):
        try:
            fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
            client = fb.client.create(
                client={
                    'email': user.email,
                    'username': user.username,
                    'password': user.password
                }
            )
            # create instance
            client = cls(user=user, email=user.email, freshbooks_id=client.client_id)
            return client
        except Exception as e:
            print e
            return None

    def update_info(self, **kwargs):
        fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
        response = fb.invoice.create(
            invoice=dict(
                client_id= self.freshbooks_id,
            )
        )
        print response


# Freshbooks Invoice Manager

class InvoiceManager(models.Manager):
    def create_invoice(self, user):
        try:
            client = Client.objects.get(user=user)
            fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
            resp = fb.invoice.create(
                invoice=dict(
                    client_id= client.freshbooks_id,
                )
            )
            new_invoice = self.create(
                client = client,
                freshbooks_id = resp.invoice_id,
            )
            return new_invoice
        except ObjectDoesNotExist as e:
            print 'Invoice Creation Error %s' % (e)
            return None
        except Exception as e:
            print 'Invoice Creation Error %s' % (e)
            return None

    def send_bills(self):
        for invoice in self.filter(status='BL'):
            invoice.send_bill()

    def pending(self, user):
        try:
            client = Client.objects.get(user=user)
            latest = self.filter(client=client).latest('date_created')
            if latest.is_pending():
                return latest
            else:
                new_invoice = self.create_invoice(user)
                return new_invoice
        except ObjectDoesNotExist as e:
            print 'Invoice Creation Error %s' % (e)
            return None


# Freshbooks Invoice Model

class Invoice(models.Model):
    client = models.ForeignKey(Client)
    freshbooks_id = models.CharField(max_length=10000)
    date_created = models.DateField(auto_now=True)
    date_sent = models.DateField()
    status = models.CharField(max_length=2, choices=STATUSES, default='CR')
    objects = InvoiceManager()

    def add_line(self, order):
        if order.is_local:
            order_type = 'Local'
        else:
            order_type = 'Non-Local'
        fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
        fb.invoice.lines.add(
            invoice_id = self.freshbooks_id,
            lines = [
                api.types.line(
                    name = order_type + ' Delivery',
                    description = str(order),
                    unit_cost = order.price,
                    quantity=1
                )
            ]
        )
        self.status = 'BL'

    def send_bill(self):
        if self.status == 'BL':
            fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
            fb.invoice.sendByEmail(invoice_id= self.freshbooks_id)
            self.status = 'SE'
            self.date_sent = datetime.date.today()

    def is_pending(self):
        if self.status == 'CR' or 'BL':
            return True
        else:
            return False

    def get_amount(self):
        try:
            fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
            resp = fb.invoice.get(invoice_id= self.freshbooks_id)
            return resp.invoice.amount
        except Exception:
            return None
