from django.views.generic import View, ListView, FormView, TemplateView
from django.shortcuts import render

from delivery.models import Order
from .models import Invoice
from .forms import ClientForm

# Create your views here.


class BalanceView(TemplateView):
    template_name = 'invoicing/balance.html'

    def get_context_data(self, **kwargs):
        orders = Order.objects.exclude(price__isnull=True)#.filter(status='DE')
        balance = 0
        for order in orders:
            balance += order.price
            print order
        return {
            'lines': orders,
            'balance': balance
        }

    def post(self, request, *args, **kwargs):
        latest_invoice = Invoice.objects.pending(self.request.user)
        latest_invoice.send_bill()


class ClientView(FormView):
    template_name = 'invoicing/client.html'
    form_class = ClientForm


class HistoryView(ListView):
    template_name = 'invoicing/history.html'
    model = Invoice
    title = 'My Invoices'
