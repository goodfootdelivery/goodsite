from django.core.management.base import BaseCommand, CommandError
from invoicing.models import Invoice


class Command(BaseCommand):
    help = 'Send all outstanding invoices via email.'
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Invoice.objects.send_bills()
