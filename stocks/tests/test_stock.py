from unittest.mock import patch

import pandas as pd
from django.test import TestCase

from stocks.models import Stock


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
        # when
        Stock.objects.initialize_stocks()

        # then
        self.assertTrue(Stock.objects.filter(code="005930").exists())
        self.assertTrue(Stock.objects.filter(code="373220").exists())
