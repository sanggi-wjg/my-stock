from unittest import TestCase

from mystock.core.constants import INDEXES
from stocks.models import Stock
from stocks.tests.test_base import TestBase


class TestStock(TestBase):
    def test_initialize_stocks(self):
        # given
        Stock.objects.initialize_stocks()
        self.assert_true(Stock.objects.count() == 2)

        # when
        Stock.objects.initialize_stocks()
        self.assert_true(Stock.objects.count() == 2)

        # then
        self.assert_true(Stock.objects.filter(code="005930").exists())
        self.assert_true(Stock.objects.filter(code="373220").exists())

    def test_initialize_stock_indexes(self):
        # given
        Stock.objects.initialize_stock_indexes()
        self.assert_true(len(INDEXES) == Stock.objects.filter_index().count())

        # when
        Stock.objects.initialize_stock_indexes()
        self.assert_true(len(INDEXES) == Stock.objects.filter_index().count())

        # then
        for code, name in INDEXES:
            self.assert_true(Stock.objects.filter(code=code, name=name).exists())
