from typing import List, Tuple

import pandas as pd
from django.core.management import BaseCommand
from matplotlib import pyplot as plt

from mystock.core.utils import get_now_text
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
        dataset = StockPrice.objects.filter(stock__name__in=targets)
        df = pd.DataFrame(
            [p.price_close for p in dataset],
            index=[p.date for p in dataset],
            columns=["Price"],
        )

        # plt.rcParams["font.family"] = "NanumBarunGothic"
        plt.rcParams["figure.figsize"] = (70, 30)
        plt.rcParams["lines.linewidth"] = 4
        plt.rcParams["font.size"] = 40
        plt.rcParams["axes.grid"] = True
        plt.rcParams["grid.linestyle"] = "--"
        plt.rcParams["grid.linewidth"] = 2

        fig = plt.figure(tight_layout=True)
        ax1 = fig.add_subplot(111)
        ax1.set_ylabel("Price")

        lines = []

        for i, p in enumerate(df):
            line = ax1.plot(df, color=plt_colors(i), label=df)
            lines.append(line)

            first, last = str(df.index[0]), str(df.index[-1])
            for crisis in financial_crises():
                if first <= crisis[0] and crisis[1] <= last:
                    ax1.axvspan(crisis[0], crisis[1], color="gray", alpha=0.2)

            ax1.legend([x[0] for x in lines], targets, loc="upper left")
            plt.grid(
                True, which="both", axis="x", color="gray", alpha=0.3, linestyle="--"
            )
            plt.show()
            plt.close(fig)


def financial_crises() -> List[Tuple[str, str, str]]:
    """
    :return: 경제 위기 리스트 start date, end date, crisis 이름
    :rtype: List[Tuple[str, str, str]]
    """
    return [
        ("1983-09-24", "1983-10-17", "검은 토요일"),
        ("1987-07-19", "1988-01-31", "검은 월요일"),
        ("1997-01-01", "1997-12-31", "동 아시아 외환 위기"),
        ("2000-01-01", "2001-03-30", "IT 버블"),
        ("2001-09-11", "2001-12-31", "미국 911 테러"),
        ("2007-12-01", "2009-03-30", "서브 프라임 모기지"),
        ("2010-03-01", "2011-11-01", "유럽 금융 위기"),
        ("2015-08-11", "2016-03-01", "위완화 평가 절하 발표"),
        ("2020-02-21", "2020-03-23", "우한 폐렴 전설의 시작"),
        ("2021-09-18", "2021-10-01", "헝다 그룹 파산"),
        ("2022-02-24", "2022-03-01", "러시아 우크라이나 침공"),
    ]


# def plt_year_format() -> Tuple[YearLocator, DateFormatter]:
#     return dates.YearLocator(), dates.DateFormatter("%Y")
#
#
# def plt_year_month_format() -> Tuple[MonthLocator, DateFormatter]:
#     return dates.MonthLocator(), dates.DateFormatter("%Y-%M")
#
def plt_colors(no) -> str:
    colors = ["blue", "green", "red", "cyan", "magenta", "yellow"]
    return colors[no % len(colors)]
