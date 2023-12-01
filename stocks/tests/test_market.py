from django.test import TestCase

from mystock.core.constants import ALLOWED_MARKETS
from stocks.models import Market


class MarketTestCase(TestCase):
    def setUp(self):
        Market.objects.initialize_markets()

    def test_is_exists_market(self):
        # given
        market_names = ALLOWED_MARKETS

        # when
        for name in market_names:
            # then
            self.assertTrue(Market.objects.is_exists_market(name))
