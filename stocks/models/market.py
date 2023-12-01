from django.db import models

from mystock.core.constants import ALLOWED_MARKETS


class MarketQuerySet(models.QuerySet):
    def initialize_markets(self):
        for market_name in ALLOWED_MARKETS:
            self.get_or_create(name=market_name)

    def is_exists_market(self, market_name: str):
        return self.filter(name=market_name).exists()


class Market(models.Model):
    objects = MarketQuerySet.as_manager()

    class Meta:
        db_table = "market"

    name = models.CharField(max_length=100, unique=True)
