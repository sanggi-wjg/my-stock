import math
from decimal import Decimal
from typing import List, Tuple

import pandas as pd
from django.utils import timezone
from matplotlib import dates
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.dates import YearLocator, DateFormatter, MonthLocator

from mystock.core.utils import logger


class ChartDrawer:
    def __init__(self):
        plt.rcParams["font.family"] = "Nanum Gothic"
        plt.rcParams["figure.figsize"] = (80, 40)
        plt.rcParams["lines.linewidth"] = 6
        plt.rcParams["font.size"] = 40
        plt.rcParams["axes.grid"] = True
        plt.rcParams["axes.axisbelow"] = True
        plt.rcParams["grid.linestyle"] = "--"
        plt.rcParams["grid.linewidth"] = 4

        self.fig = plt.figure(layout="tight")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylabel("Price")

        plt.grid(True, which="both", axis="x", color="gray", alpha=0.3, linestyle="--")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        plt.close(self.fig)

    @property
    def financial_crises(self) -> List[Tuple[str, str, str]]:
        return get_financial_crises()

    def draw_financial_crises(self, dfs: List[pd.DataFrame], i: int, ax: Axes):
        first, last = str(dfs[i].index[0]), str(dfs[i].index[-1])

        for crisis in self.financial_crises:
            if first <= crisis[0] and crisis[1] <= last:
                self.ax.axvspan(crisis[0], crisis[1], color="gray", alpha=0.2)

    def draw_stock_prices(self, dfs: List[pd.DataFrame], legend: List[str]):
        lines = []

        for i, p in enumerate(dfs):
            lines.append(self.ax.plot(dfs[i], color=plt_colors(i), label=dfs[i]))
            self.draw_financial_crises(dfs, i, self.ax)

        self.ax.legend([x[0] for x in lines], legend, loc="upper left")

    def draw(self, dfs: List[pd.DataFrame], legend: List[str]):
        fname = f"{'_'.join(legend)}_{current_time_to_text()}.png"
        self.draw_stock_prices(dfs, legend)
        self.fig.savefig(fname)

    def show(self):
        self.fig.show()


def current_time_to_text(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    return timezone.now().strftime(date_format)


def check_nan_return_or_zero(value) -> Decimal:
    return Decimal(value) if not math.isnan(value) else Decimal("0")


def get_financial_crises() -> List[Tuple[str, str, str]]:
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
        ("2021-09-18", "2021-12-28", "헝다 그룹 파산"),
        ("2022-02-24", "2022-05-31", "러시아 우크라이나 침공"),
    ]


def plt_year_format() -> Tuple[YearLocator, DateFormatter]:
    return dates.YearLocator(), dates.DateFormatter("%Y")


def plt_year_month_format() -> Tuple[MonthLocator, DateFormatter]:
    return dates.MonthLocator(), dates.DateFormatter("%Y-%M")


#
def plt_colors(no) -> str:
    colors = ["blue", "green", "red", "cyan", "magenta", "yellow"]
    return colors[no % len(colors)]


def debug_fonts():
    import matplotlib.font_manager as fm

    f = [f.name for f in fm.fontManager.ttflist]
    logger.debug(f)


def earning_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    수익률
    :return: 수익률 df
    :rtype: pd.DataFrame
    """
    df = (df / df.iloc[0]) - Decimal(1.0)
    return df


def standardize(df: pd.DataFrame) -> pd.DataFrame:
    """
    표준화 https://sanggi-jayg.tistory.com/entry/%ED%86%B5%EA%B3%84-%EC%A0%95%EA%B7%9C%ED%99%94Normalization%EC%99%80-%ED%91%9C%EC%A4%80%ED%99%94Standardization

    [Default Formula]
    Standard Score = (raw value - mean) / std

    :return: 표준화 df
    :rtype: pd.DataFrame
    """
    df["Price"] = pd.to_numeric(df["Price"])
    mean, std = df.mean(axis=0), df.std(axis=0)
    return (df["Price"] - mean["Price"]) / std["Price"]


def normalize(
    df: pd.DataFrame, range_a: float = 0.0, range_b: float = 1.0
) -> pd.DataFrame:
    """
    정규화 https://sanggi-jayg.tistory.com/entry/%ED%86%B5%EA%B3%84-%EC%A0%95%EA%B7%9C%ED%99%94Normalization%EC%99%80-%ED%91%9C%EC%A4%80%ED%99%94Standardization

    Use Min-max feature scaling formula, this can be generalized to restrict of values in dataset

    [Default formula]
    Normalized Value = (raw value - min) / (max - min)

    [If you want specific range, apply this formula]
    Normalized Value = (raw value - min) / (max - min) * (range_b - range_a) + range_a

    :return: 정규화 df
    :rtype: pd.DataFrame
    """
    df["Price"] = pd.to_numeric(df["Price"])
    max_ax, min_ax = df.max(axis=0), df.min(axis=0)
    normalized_value = (df["Price"] - min_ax["Price"]) / (
        max_ax["Price"] - min_ax["Price"]
    )
    return normalized_value * (range_b - range_a) + range_a
