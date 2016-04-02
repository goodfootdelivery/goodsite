from django.views.generic import View, ListView, UpdateView, TemplateView
from django.shortcuts import render

from delivery.models import Order
from .models import Invoice
from .forms import ClientForm


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
        # Change Order statuses
        orders = Order.objects.filter(
            user=self.request.user,
        ).exclude(price__isnull=True)
        for order in orders:
            order.status = 'PD'
            order.save()


class ClientView(UpdateView):
    template_name = 'invoicing/client.html'
    form_class = ClientForm
    # success_url = '/something/'

    def form_valid(self, form):
        pass


class HistoryView(ListView):
    template_name = 'invoicing/history.html'
    model = Invoice
    title = 'My Invoices'

    def get_context_data(self):
        pass
