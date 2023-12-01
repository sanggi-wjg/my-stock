from django.core.management import BaseCommand

from stocks.models import Market, Stock


class Command(BaseCommand):
    def handle(self, *args, **options):
        Market.objects.initialize_markets()

        markets = Market.objects.filter_stock()
        for market in markets:
            Stock.objects.initialize_stocks(market.name)
