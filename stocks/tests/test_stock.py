from unittest import TestCase

from mystock.core.constants import INDEXES
from stocks.models import Stock
from stocks.tests.test_base import TestBase


class TestStock(TestBase):
    def test_initialize_stocks(self):
        # given
        Stock.objects.initialize_stocks()
        assert Stock.objects.count() == 8

        # when
        Stock.objects.initialize_stocks()
        assert Stock.objects.count() == 8

        # then
        assert Stock.objects.filter(code="005930").exists()
        assert Stock.objects.filter(code="373220").exists()

    def test_initialize_stock_indexes(self):
        # given
        Stock.objects.initialize_stock_indexes()
        assert Stock.objects.filter_index().count() == len(INDEXES)

        # when
        Stock.objects.initialize_stock_indexes()
        assert Stock.objects.filter_index().count() == len(INDEXES)

        # then
        for code, name in INDEXES:
            assert Stock.objects.filter(code=code, name=name).exists()
