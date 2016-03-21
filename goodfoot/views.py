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
