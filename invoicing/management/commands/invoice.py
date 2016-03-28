from django.core.management.base import BaseCommand, CommandError
from invoicing.models import Invoice


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
