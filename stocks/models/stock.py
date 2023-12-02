import FinanceDataReader as fdr
from django.db import models


class StockQuerySet(models.QuerySet):
    def initialize_stocks(self, market_name: str):
        from stocks.models import Market

        market = Market.objects.get(name=market_name)
        exist_stock_codes = self.get_all_codes()

        dataset = fdr.StockListing(market.name)
        not_exist_stocks = [
            row
            for date, row in dataset.iterrows()
            if row["Code"] not in exist_stock_codes
        ]

        new_stocks = [
            Stock(code=row["Code"], name=row["Name"], market=market)
            for row in not_exist_stocks
        ]
        self.bulk_create(new_stocks, batch_size=500)

    def get_all_codes(self) -> list[str]:
        return self.values_list("code", flat=True).all()


class Stock(models.Model):
    objects = StockQuerySet.as_manager()

    class Meta:
        db_table = "stock"
        constraints = [
            models.UniqueConstraint(
                fields=["market", "code"],
                name="unique_stock_001",
            ),
            models.UniqueConstraint(
                fields=["market", "name"],
                name="unique_stock_002",
            ),
        ]

    code = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=100, db_index=True)

    # relation
    market = models.ForeignKey(
        to="Market",
        related_name="stocks",
        on_delete=models.PROTECT,
    )
