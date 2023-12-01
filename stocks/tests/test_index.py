from django.test import TestCase

from mystock.core.constants import ALLOW_INDEXES
from stocks.models import Market, Index


class IndexTestCase(TestCase):
    def setUp(self):
        Index.objects.initialize_indexes()

    def test_is_exists_market(self):
        # given
        index_names = ALLOW_INDEXES

        # when
        for name in index_names:
            # then
            self.assertTrue(Index.objects.is_exists_index(name))
