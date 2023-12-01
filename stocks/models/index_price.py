from decimal import Decimal

from django.db import models


class IndexPriceQuerySet(models.QuerySet):
    pass


class IndexPrice(models.Model):
    objects = IndexPriceQuerySet.as_manager()

    class Meta:
        db_table = "index_price"
        constraints = [
            models.UniqueConstraint(
                fields=["index", "date"],
                name="unique_index_price_001",
            )
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
    index = models.ForeignKey(
        to="Index", related_name="prices", on_delete=models.PROTECT
    )
