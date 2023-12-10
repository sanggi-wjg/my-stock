from typing import List

from django.db import models
from django.db.models import Q

from mystock.core.constants import INDEXES, DEFAULT_BATCH_SIZE
from mystock.core.fdr_client import StockFdr


class StockMarketEnum(models.TextChoices):
    # 한국
    KOSPI = "KOSPI"
    KOSDAQ = "KOSDAQ"
    # 미국
    SNP500 = "S&P500"
    NASDAQ = "NASDAQ"
    # 인덱스
    GLOBAL_INDEX = "GLOBAL_INDEX"

    def is_index(self):
        return self == self.GLOBAL_INDEX

    def is_use_code(self):
        return self in [
            StockMarketEnum.KOSPI,
            StockMarketEnum.KOSDAQ,
        ]

    def is_use_ticker(self):
        return self in [
            StockMarketEnum.SNP500,
            StockMarketEnum.NASDAQ,
        ]


class StockTypeEnum(models.TextChoices):
    STOCK = "STOCK"
    INDEX = "INDEX"


class StockQuerySet(models.QuerySet):
    def initialize_stocks(self):
        market_enum: StockMarketEnum

        for market_enum in StockMarketEnum:
            if market_enum.is_index():
                continue

            market_name = market_enum.value
            exist_stock_codes = self.filter(
                type=StockTypeEnum.STOCK, market=market_name
            ).values_list("code", flat=True)

            not_exist_stocks = []
            dataset = StockFdr.stock_listing(market_name)

            if market_enum.is_use_code():
                not_exist_stocks = [
                    row
                    for date, row in dataset.iterrows()
                    if row["Code"] not in exist_stock_codes
                ]

            if market_enum.is_use_ticker():
                not_exist_stocks = [
                    row
                    for date, row in dataset.iterrows()
                    if row["Symbol"] not in exist_stock_codes
                ]

            new_stocks = [
                Stock(
                    market=market_name,
                    type=StockTypeEnum.STOCK,
                    code=row["Code"] if market_enum.is_use_code() else row["Symbol"],
                    name=row["Name"],
                )
                for row in not_exist_stocks
            ]
            self.bulk_create(new_stocks, batch_size=DEFAULT_BATCH_SIZE)

    def initialize_stock_indexes(self):
        exist_index_codes = self.filter(
            type=StockTypeEnum.INDEX,
            code__in=(code for (code, _) in INDEXES),
        ).values_list("code", flat=True)

        not_exist_indexes = [
            (code, name) for (code, name) in INDEXES if code not in exist_index_codes
        ]

        new_indexes = [
            Stock(
                market=StockMarketEnum.GLOBAL_INDEX,
                type=StockTypeEnum.INDEX,
                code=code,
                name=name,
            )
            for (code, name) in not_exist_indexes
        ]
        self.bulk_create(new_indexes, batch_size=DEFAULT_BATCH_SIZE)

    def filter_stock(self):
        return self.filter(type=StockTypeEnum.STOCK)

    def filter_index(self):
        return self.filter(type=StockTypeEnum.INDEX)

    def filter_markets(self, markets: List[str]):
        return self.filter(market__in=markets)

    def filter_names(self, names: List[str]):
        return self.filter(Q(name__in=names) | Q(code__in=names))

    def exclude_nasdaq(self):
        return self.exclude(market=StockMarketEnum.NASDAQ)


class Stock(models.Model):
    objects = StockQuerySet.as_manager()

    class Meta:
        db_table = "stock"
        constraints = [
            models.UniqueConstraint(
                fields=["market", "code", "name"],
                name="unique_stock_001",
            ),
        ]

    market = models.CharField(max_length=50, choices=StockMarketEnum.choices)
    type = models.CharField(max_length=50, choices=StockTypeEnum.choices)
    code = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
