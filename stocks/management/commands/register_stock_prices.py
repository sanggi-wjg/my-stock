from datetime import datetime

import FinanceDataReader as fdr
import pandas as pd
from django.core.management import BaseCommand
from django.db.models import Q

from mystock.core.utils import logger
from mystock.core.utils_chart import check_nan_return_or_zero
from stocks.models import Stock, StockPrice

log = logger


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--markets", nargs="+", type=str, default=[], required=False
        )
        """
        --markets KOSPI, S&P500
        """

    def handle(self, *args, **options):
        stocks = Stock.objects.exclude_nasdaq()
        if len(options["markets"]) > 0:
            stocks = stocks.filter_markets(options["markets"])

        for stock in stocks:
            last_stock_price = StockPrice.objects.find_recent_of_stock(stock)

            if last_stock_price is None:
                dataset = fdr.DataReader(stock.code, "1980-01-01")
            else:
                dataset = fdr.DataReader(stock.code, last_stock_price.next_update_date)

            new_stock_prices = self.parse_to_stock_prices(stock, dataset)
            StockPrice.objects.bulk_create(new_stock_prices, batch_size=1000)
            log.info(f"{stock.name} created, rows: {len(new_stock_prices)}.")

    def parse_to_stock_prices(self, stock, dataset: pd.DataFrame):
        new_stock_prices = []
        for date, row in dataset.iterrows():
            price_open = check_nan_return_or_zero(row.get("Open", 0))
            price_close = check_nan_return_or_zero(row.get("Close", 0))
            price_high = check_nan_return_or_zero(row.get("High", 0))
            price_low = check_nan_return_or_zero(row.get("Low", 0))
            price_change = check_nan_return_or_zero(row.get("Change", 0))

            is_nothing = all(
                [price_open == 0, price_close == 0, price_high == 0, price_low == 0]
            )
            if is_nothing:
                continue

            new_stock_prices.append(
                StockPrice(
                    date=datetime.strptime(date.strftime("%y-%m-%d"), "%y-%m-%d"),
                    price_open=price_open,
                    price_close=price_close,
                    price_high=price_high,
                    price_low=price_low,
                    price_change=price_change,
                    stock=stock,
                )
            )
        return new_stock_prices
