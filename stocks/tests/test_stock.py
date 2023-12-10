from unittest import TestCase

from stocks.models import Stock
from stocks.tests.test_base import TestBase


class TestStock(TestBase):
    def test_initialize(self):
        # given
        Stock.objects.initialize_stocks()

        # then
        self.assert_true(Stock.objects.count() == 2)
        self.assert_true(Stock.objects.filter(code="005930").exists())
        self.assert_true(Stock.objects.filter(code="373220").exists())
