from django.dispatch import Signal

# Order Purchased Event
order_purchased = Signal(
    providing_args=[ 'order_id', 'price', 'order_str' ]
)
