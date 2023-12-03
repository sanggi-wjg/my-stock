from unittest.mock import patch

import pandas as pd
from django.test import TestCase

from mystock.core.constants import MARKET_TYPE_STOCK
from stocks.models import Stock, Market


class StockTestCase(TestCase):
    def setUp(self):
        pass

    @patch(
        "mystock.core.fdr_client.StockFdr.stock_listing",
        return_value=pd.DataFrame(
            [
                ["005930", "삼성전자"],
                ["373220", "LG에너지솔루션"],
            ],
            columns=["Code", "Name"],
        ),
    )
    def test_initialize(self, mock):
        # given
        market = Market.objects.create(type=MARKET_TYPE_STOCK, name="KOSPI")

        # when
        Stock.objects.initialize_stocks(market.name)

        # then
        self.assertTrue(Stock.objects.filter(code="005930").exists())
        self.assertTrue(Stock.objects.filter(code="373220").exists())
