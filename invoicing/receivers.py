from django.dispatch import receiver

from account.signals import password_changed
from account.signals import user_sign_up_attempt, user_signed_up
from account.signals import user_login_attempt, user_logged_in

from pinax.eventlog.models import log

from delivery.models import Order
from delivery.signals import order_purchased, test_signal
from invoicing.models import Client


# Handle When Order Is Purchased

@receiver(order_purchased, sender=Order)
def handle_order_purchased(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="ORDER_PURCHSED",
        extra={}
    )


@receiver(test_signal)
def handle_test_signal(sender, **kwargs):
    print '\n'
    print 'TEST SIGNAL RECEIVED'
    print '\n'


# Create New Client on Initial Login

@receiver(user_signed_up)
def handle_client_creation(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="USER_SIGNED_UP",
        extra={}
    )
    print 'CREATE CLIENT'
