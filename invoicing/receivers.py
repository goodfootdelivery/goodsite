from django.dispatch import receiver

# from account.signals import email_confirmed, user_signed_up
# from pinax.eventlog.models import log

from delivery.models import Order
from delivery.signals import order_purchased
from invoicing.models import Client, Invoice


# Handle When Order Is Purchased

@receiver(order_purchased, sender=Order)
def handle_order_purchased(sender, **kwargs):
    order = kwargs.get('order')
    user = order.user
    log(
        user=user,
        action="ORDER_PURCHSED",
        extra={ 'order': order.id }
    )
    latest_invoice = Invoice.objects.pending(user)
    order = latest_invoice.add_line(order)
    # Query If Request Passed
    if order:
        order.save()
