from django.views.generic import View, ListView, FormView, TemplateView
from django.shortcuts import render

from delivery.models import Order
from .models import Invoice
from .forms import ClientForm

# Create your views here.


class BalanceView(View):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.exclude(price__isnull=True).filter(status='DE')
        balance = 0
        for order in orders:
            balance += order.price
        return {
            'invoices': orders,
            'balance': balance
        }
        pass

    def post(self, request, *args, **kwargs):
        pass


class ClientView(FormView):
    template_name = 'invoicing/client.html'
    form_class = ClientForm


class HistoryView(TemplateView):
    template_name = 'invoicing/history.html'
    # model = Invoice
    title = 'My Invoices'
