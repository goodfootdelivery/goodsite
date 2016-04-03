from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from delivery.models import Order
from account import views, forms

# Homepage

class HomeView(TemplateView):
    template_name = 'homepage.html'


# Account Views


class LoginView(views.LoginView):
    form_class = forms.LoginEmailForm


# Delivery Views


class DeliveryFormView(TemplateView):
    template_name = 'delivery/orderForm.html'
    title = 'home'


class DeliveryDetailView(DetailView):
    template_name = 'delivery/orderDetail.html'
    model = Order


class DeliveryHubView(ListView):
    template_name = 'delivery/orderHub.html'
    model = Order
    title = 'My Orders'

    def get_context_data(self, **kwargs):
        orders = Order.objects.filter(
            user=self.request.user,
        ).exclude(price__isnull=True)
        balance = 0
        for order in orders:
            balance += order.price
        return {
            'order_list': orders,
            'balance': balance
        }
