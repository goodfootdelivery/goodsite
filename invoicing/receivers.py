from django.dispatch import receiver

from account.signals import email_confirmed, user_signed_up
from pinax.eventlog.models import log

from delivery.models import Order
from delivery.signals import order_purchased
from invoicing.models import Client, Invoice


# Handle When Order Is Purchased

@receiver(order_purchased, sender=Order)
def handle_order_purchased(sender, **kwargs):
    order = kwargs.get('order')
    owner = order.owner
    log(
        user=owner,
        action="ORDER_PURCHSED",
        extra={ 'order': order.id }
    )
    latest_invoice = Invoice.objects.pending(owner)
    latest_invoice.add_line(order)


# Create New Client on Initial Login
@receiver(user_signed_up)
def handle_user_signed_up(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="USER_SIGNED_UP",
        extra={}
    )
    client = Client.register(kwargs.get("user"))
    client.save()


# Verify Client upon Email Confirmation
@receiver(email_confirmed)
def handle_email_confirmed(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="USER_SIGNED_UP",
        extra={}
    )
    print 'CREATE CLIENT'
