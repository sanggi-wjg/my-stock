from django.core.management import BaseCommand

from stocks.models import Stock


class Command(BaseCommand):
    def handle(self, *args, **options):
        Stock.objects.initialize_stock_indexes()
        Stock.objects.initialize_stocks()
