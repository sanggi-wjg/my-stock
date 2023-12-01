from django.core.management import BaseCommand

from stocks.models import Market, Stock


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--market", type=str, required=True)

    def handle(self, *args, **options):
        market_name = options.get("market", "").upper()
        if not Market.objects.is_exists_market(market_name):
            raise Exception(f"Market {market_name} does not exist.")

        Stock.objects.initialize_stocks(market_name)
