import math
from datetime import timedelta, datetime
from decimal import Decimal

import FinanceDataReader as fdr
from django.core.management import BaseCommand

from mystock.core.utils import check_nan_return_or_zero
from stocks.models import Stock, StockPrice


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--stocks", nargs="+", type=str, required=True)

    def handle(self, *args, **options):
        stocks = Stock.objects.filter(name__in=options.get("stocks", []))
        new_stock_prices = []

        for stock in stocks:
            last_stock_price = StockPrice.objects.find_recent_by_stock(stock)

            if last_stock_price is None:
                dataset = fdr.DataReader(stock.code, "1980-01-01")
            else:
                dataset = fdr.DataReader(stock.code, last_stock_price.next_update_date)

            new_stock_prices.extend(
                [
                    StockPrice(
                        date=datetime.strptime(date.strftime("%y-%m-%d"), "%y-%m-%d"),
                        price_open=Decimal(row["Open"]),
                        price_close=Decimal(row["Close"]),
                        price_high=Decimal(row["High"]),
                        price_low=Decimal(row["Low"]),
                        price_change=check_nan_return_or_zero(row["Change"]),
                        stock=stock,
                    )
                    for date, row in dataset.iterrows()
                ]
            )

        StockPrice.objects.bulk_create(new_stock_prices, batch_size=500)
