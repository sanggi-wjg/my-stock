from dataclasses import dataclass
from typing import List

import pandas as pd
from django.core.management import BaseCommand

from mystock.core.utils import (
    get_now_text,
    logger,
    standardize,
    normalize,
    earning_rate,
    ChartDrawer,
)
from stocks.models import StockPrice


@dataclass(order=True, slots=True, frozen=True)
class _CommandOption:
    targets: List[str]
    start_date: str
    end_date: str
    is_standardize: bool
    is_normalize: bool
    normalize_range_a: float
    normalize_range_b: float
    is_earning_rate: bool


class Command(BaseCommand):
    def add_arguments(self, parser):
        # 날짜
        parser.add_argument("--start", default="1980-01-01", type=str)
        parser.add_argument("--end", default=get_now_text("%Y-%m-%d"), type=str)

        # 표준화, 정규화, 수익률
        parser.add_argument("-s", "--standardize", default=False, type=bool, help="표준화")
        parser.add_argument("-n", "--normalize", default=False, type=bool, help="정규화")
        parser.add_argument(
            "-na", "--normalize_range_a", default=0.0, type=float, help="기본 정규화 범위 A"
        )
        parser.add_argument(
            "-nb", "--normalize_range_b", default=1.0, type=float, help="기본 정규화 범위 B"
        )
        parser.add_argument("-e", "--earning", default=False, type=bool, help="수익률")

        # Targets: 주식 or 인덱스
        parser.add_argument("-t", "--targets", nargs="+", type=str, required=True)
        """
        -t 카카오 NAVER 삼성전자 -s True
        -t KS11 KQ11 -n True
        """

    def handle(self, *args, **options):
        command_option = _CommandOption(
            targets=sorted(options.get("targets")),
            start_date=options.get("start"),
            end_date=options.get("end"),
            is_standardize=options.get("standardize"),
            is_normalize=options.get("normalize"),
            normalize_range_a=options.get("normalize_range_a"),
            normalize_range_b=options.get("normalize_range_b"),
            is_earning_rate=options.get("earning"),
        )

        dfs, stock_names = [], []

        for target_stock in command_option.targets:
            stock_prices = (
                StockPrice.objects.select_related("stock")
                .filter_stock(target_stock)
                .filter_range(command_option.start_date, command_option.end_date)
                .order_by("date")
            )
            if not stock_prices.exists():
                logger.warning(f"{target_stock} does not exist")
                command_option.targets.pop(command_option.targets.index(target_stock))
                continue

            df = pd.DataFrame(
                [p.price_close for p in stock_prices],
                index=[p.date for p in stock_prices],
                columns=["Price"],
            )
            if command_option.is_standardize:
                df = standardize(df)
            if command_option.is_normalize:
                df = normalize(
                    df,
                    command_option.normalize_range_a,
                    command_option.normalize_range_b,
                )
            if command_option.is_earning_rate:
                df = earning_rate(df)

            dfs.append(df)
            stock_names.append(stock_prices.first().stock.name)

        with ChartDrawer() as chart_drawer:
            chart_drawer.draw(dfs, stock_names)
