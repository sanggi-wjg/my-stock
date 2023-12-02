from typing import List, Tuple

import pandas as pd
from django.core.management import BaseCommand
from matplotlib import pyplot as plt

from mystock.core.utils import get_now_text, plt_colors, financial_crises, logger
from stocks.models import StockPrice


class Command(BaseCommand):
    def add_arguments(self, parser):
        # 날짜
        parser.add_argument("--start", default="1980-01-01", type=str)
        parser.add_argument("--end", default=get_now_text("%Y-%m-%d"), type=str)

        # 표준화, 정규화, 수익률
        parser.add_argument("-s", "--standard", default=False, type=bool, help="표준화")
        parser.add_argument("-n", "--normalize", default=False, type=bool, help="정규화")
        parser.add_argument("-e", "--earning", default=False, type=bool, help="수익률")

        # Targets: 주식 or 인덱스
        parser.add_argument("-t", "--targets", nargs="+", type=str, required=True)
        """
        -t NHN 카카오 NAVER
        """

    def handle(self, *args, **options):
        targets = options.get("targets", [])
        start = options.get("start")
        end = options.get("end")

        df = []
        for stock_name in targets:
            stock_prices = StockPrice.objects.filter(
                stock__name=stock_name, date__gte=start, date__lte=end
            ).order_by("date")
            if not stock_prices.exists():
                logger.warning(f"{stock_name} does not exist")

            df.append(
                pd.DataFrame(
                    [p.price_close for p in stock_prices],
                    index=[p.date for p in stock_prices],
                    columns=["Price"],
                )
            )

        plt.rcParams["font.family"] = "Nanum Gothic"
        plt.rcParams["figure.figsize"] = (70, 30)
        plt.rcParams["lines.linewidth"] = 4
        plt.rcParams["font.size"] = 40
        plt.rcParams["axes.grid"] = True
        plt.rcParams["grid.linestyle"] = "--"
        plt.rcParams["grid.linewidth"] = 2

        fig = plt.figure(layout="tight")
        ax1 = fig.add_subplot(111)
        ax1.set_ylabel("Price")

        lines = []

        for i, p in enumerate(df):
            line = ax1.plot(df[i], color=plt_colors(i), label=df[i])
            lines.append(line)

            first, last = str(df[i].index[0]), str(df[i].index[-1])
            for crisis in financial_crises():
                if first <= crisis[0] and crisis[1] <= last:
                    ax1.axvspan(crisis[0], crisis[1], color="gray", alpha=0.2)

        ax1.legend([x[0] for x in lines], targets, loc="upper left")
        plt.grid(True, which="both", axis="x", color="gray", alpha=0.3, linestyle="--")
        plt.show()
        plt.close(fig)
