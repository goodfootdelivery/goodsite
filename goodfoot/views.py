from django.views.generic import TemplateView, ListView
from delivery.models import Order


class DeliveryView(TemplateView):
    template_name = 'delivery/orderForm.html'
    title = 'home'

class HubView(ListView):
    template_name = 'delivery/orderHub.html'
    model = Order
    title = 'My Orders'
