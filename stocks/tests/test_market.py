from django.test import TestCase

from mystock.core.constants import MARKETS
from stocks.models import Market


class MarketTestCase(TestCase):
    def setUp(self):
        Market.objects.initialize_markets()

    def test_is_exists_market(self):
        # when
        for market_name in MARKETS:
            # then
            self.assertTrue(Market.objects.is_exists_market(market_name))
