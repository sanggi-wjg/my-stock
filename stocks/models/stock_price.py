from datetime import timedelta
from decimal import Decimal

from django.db import models


class StockPriceQuerySet(models.QuerySet):
    def find_recent_by_stock(self, stock):
        return self.filter(stock=stock).order_by("-date").first()

    def filter_range(self, start_date: str, end_date: str):
        return self.filter(
            date__gte=start_date,
            date__lte=end_date,
        )

    def filter_name(self, stock_name: str):
        return self.filter(stock__name=stock_name)


class StockPrice(models.Model):
    objects = StockPriceQuerySet.as_manager()

    class Meta:
        db_table = "stock_price"
        constraints = [
            models.UniqueConstraint(
                fields=["stock", "date"],
                name="unique_stock_price_001",
            ),
        ]

    date = models.DateField(db_index=True)
    price_open = models.DecimalField(
        max_digits=20, decimal_places=6, default=Decimal("0")
    )
    price_close = models.DecimalField(
        max_digits=20, decimal_places=6, default=Decimal("0")
    )
    price_high = models.DecimalField(
        max_digits=20, decimal_places=6, default=Decimal("0")
    )
    price_low = models.DecimalField(
        max_digits=20, decimal_places=6, default=Decimal("0")
    )
    price_change = models.DecimalField(
        max_digits=20, decimal_places=6, default=Decimal("0")
    )

    # relation
    stock = models.ForeignKey(
        to="Stock", related_name="prices", on_delete=models.PROTECT
    )

    @property
    def next_update_date(self):
        return self.date + timedelta(days=1)
