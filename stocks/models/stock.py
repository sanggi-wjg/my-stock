from django.db import models

from mystock.core.constants import INDEXES, DEFAULT_BATCH_SIZE
from mystock.core.fdr_client import StockFdr


class StockMarketEnum(models.TextChoices):
    # 한국
    KOSPI = "KOSPI"
    KOSDAQ = "KOSDAQ"
    # 미국
    # SNP500 = "S&P500"
    # NASDAQ = "NASDAQ"
    # 인덱스
    GLOBAL_INDEX = "GLOBAL_INDEX"


class StockTypeEnum(models.TextChoices):
    STOCK = "STOCK"
    INDEX = "INDEX"


class StockQuerySet(models.QuerySet):
    def initialize_stocks(self):
        for value, _ in StockMarketEnum.choices:
            if value == StockMarketEnum.GLOBAL_INDEX:
                continue

            exist_stock_codes = self.filter(type=StockTypeEnum.STOCK).values_list(
                "code", flat=True
            )

            dataset = StockFdr.stock_listing(value)
            not_exist_stocks = [
                row
                for date, row in dataset.iterrows()
                if row["Code"] not in exist_stock_codes
            ]

            new_stocks = [
                Stock(
                    market=value,
                    type=StockTypeEnum.STOCK,
                    code=row["Code"],
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
