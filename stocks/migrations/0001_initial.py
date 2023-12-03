# Generated by Django 4.2.7 on 2023-12-03 10:24

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Stock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "market",
                    models.CharField(
                        choices=[
                            ("KOSPI", "Kospi"),
                            ("KOSDAQ", "Kosdaq"),
                            ("GLOBAL_INDEX", "Global Index"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("STOCK", "Stock"), ("INDEX", "Index")], max_length=50
                    ),
                ),
                ("code", models.CharField(db_index=True, max_length=50, null=True)),
                ("name", models.CharField(db_index=True, max_length=100)),
            ],
            options={
                "db_table": "stock",
            },
        ),
        migrations.CreateModel(
            name="StockPrice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(db_index=True)),
                (
                    "price_open",
                    models.DecimalField(
                        decimal_places=6, default=Decimal("0"), max_digits=20
                    ),
                ),
                (
                    "price_close",
                    models.DecimalField(
                        decimal_places=6, default=Decimal("0"), max_digits=20
                    ),
                ),
                (
                    "price_high",
                    models.DecimalField(
                        decimal_places=6, default=Decimal("0"), max_digits=20
                    ),
                ),
                (
                    "price_low",
                    models.DecimalField(
                        decimal_places=6, default=Decimal("0"), max_digits=20
                    ),
                ),
                (
                    "price_change",
                    models.DecimalField(
                        decimal_places=6, default=Decimal("0"), max_digits=20
                    ),
                ),
                (
                    "stock",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="prices",
                        to="stocks.stock",
                    ),
                ),
            ],
            options={
                "db_table": "stock_price",
            },
        ),
        migrations.AddConstraint(
            model_name="stock",
            constraint=models.UniqueConstraint(
                fields=("market", "code", "name"), name="unique_stock_001"
            ),
        ),
        migrations.AddConstraint(
            model_name="stockprice",
            constraint=models.UniqueConstraint(
                fields=("stock", "date"), name="unique_stock_price_001"
            ),
        ),
    ]
