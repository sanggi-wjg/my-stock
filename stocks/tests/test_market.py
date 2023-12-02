from django.test import TestCase

from mystock.core.constants import MARKETS, MARKET_TYPE_STOCK
from stocks.models import Market


class MarketTestCase(TestCase):
    def setUp(self):
        pass

    def test_is_exists_market(self):
        # given
        market_name = "KOSPI"
        Market(type=MARKET_TYPE_STOCK, name=market_name).save()

        # when
        is_exists = Market.objects.is_exists_market(market_name)

        # then
        self.assertTrue(is_exists)
