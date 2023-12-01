from django.db import models

from mystock.core.constants import MARKETS, MARKET_TYPE_INDEX, MARKET_TYPE_STOCK


class MarketTypeEnum(models.TextChoices):
    MARKET_TYPE_STOCK = MARKET_TYPE_STOCK, MARKET_TYPE_STOCK
    MARKET_TYPE_INDEX = MARKET_TYPE_INDEX, MARKET_TYPE_INDEX


class MarketQuerySet(models.QuerySet):
    def initialize_markets(self):
        for market_name, market_type in MARKETS:
            self.get_or_create(name=market_name, type=market_type)

    def is_exists_market(self, market_name: str):
        return self.filter(name=market_name).exists()

    def filter_stock(self):
        return self.filter(type=MARKET_TYPE_STOCK)

    def filter_index(self):
        return self.filter(type=MARKET_TYPE_INDEX)


class Market(models.Model):
    objects = MarketQuerySet.as_manager()

    class Meta:
        db_table = "market"

    type = models.CharField(max_length=100, choices=MarketTypeEnum.choices)
    name = models.CharField(max_length=100, unique=True)
