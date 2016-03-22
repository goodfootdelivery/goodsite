from django.views.generic import TemplateView, ListView
from applications.delivery.models import Order


# Delivery Form View

class DeliveryView(TemplateView):
    template_name = 'delivery/orderForm.html'
    title = 'home'


# Account Page View

class HubView(ListView):
    template_name = 'delivery/orderHub.html'
    model = Order
    title = 'My Orders'

    def get_context_data(self, **kwargs):
        orders = Order.objects.exclude(price__isnull=True)
        balance = 0
        for order in orders:
            balance += order.price
        return {
            'order_list': orders,
            'balance': balance
        }
