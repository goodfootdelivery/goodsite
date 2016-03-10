from django.views.generic import TemplateView, ListView
from api.models import Order


class HomeView(TemplateView):
    template_name = 'homepage.html'
    title = 'home'

class HubView(ListView):
    template_name = 'my_orders.html'
    model = Order
    title = 'My Orders'
