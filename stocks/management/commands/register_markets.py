from django.core.management import BaseCommand

from stocks.models import Market


class Command(BaseCommand):
    def handle(self, *args, **options):
        Market.objects.initialize_markets()
