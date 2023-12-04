import logging
import math
from decimal import Decimal
from typing import List, Tuple

import pandas as pd
from django.utils import timezone
from matplotlib import dates
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.dates import YearLocator, DateFormatter, MonthLocator


class MyLogger:
    def __init__(self):
        formatter = logging.Formatter(
            "[%(levelname)s]\t %(asctime)s\t %(pathname)s:%(lineno)d\t\t %(message)s",
            datefmt="%Y-%m-%d %I:%M:%S",
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        self.debug_logger = logging.getLogger("logger.debug")
        self.debug_logger.setLevel(logging.DEBUG)
        self.debug_logger.addHandler(stream_handler)

        self.info_logger = logging.getLogger("logger.info")
        self.info_logger.setLevel(logging.DEBUG)
        self.info_logger.addHandler(stream_handler)

        self.warn_logger = logging.getLogger("logger.warn")
        self.warn_logger.setLevel(logging.DEBUG)
        self.warn_logger.addHandler(stream_handler)

        self.error_logger = logging.getLogger("logger.error")
        self.error_logger.setLevel(logging.DEBUG)
        self.error_logger.addHandler(stream_handler)

    def debug(self, msg):
        self.debug_logger.debug(msg)

    def info(self, msg):
        self.info_logger.info(msg)

    def warning(self, msg):
        self.warn_logger.warning(msg)

    def error(self, msg):
        self.error_logger.error(msg)


logger = MyLogger()


def check_nan_return_or_zero(value) -> Decimal:
    return Decimal(value) if not math.isnan(value) else Decimal("0")


def get_now_text(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    return timezone.now().strftime(date_format)


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
        ("2021-09-18", "2021-10-01", "헝다 그룹 파산"),
        ("2022-02-24", "2022-03-01", "러시아 우크라이나 침공"),
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


class ChartDrawer:
    def __init__(self):
        plt.rcParams["font.family"] = "Nanum Gothic"
        plt.rcParams["figure.figsize"] = (70, 30)
        plt.rcParams["lines.linewidth"] = 6
        plt.rcParams["font.size"] = 40
        plt.rcParams["axes.grid"] = True
        plt.rcParams["axes.axisbelow"] = True
        plt.rcParams["grid.linestyle"] = "--"
        plt.rcParams["grid.linewidth"] = 4

        self.fig = plt.figure(layout="tight")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylabel("Price")

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
        self.draw_stock_prices(dfs, legend)

        plt.grid(True, which="both", axis="x", color="gray", alpha=0.3, linestyle="--")
        plt.show()
        plt.close(self.fig)


def earning_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    수익률
    :return: 수익률
    """
    df = (df / df.iloc[0]) - Decimal(1.0)
    return df


def standardize(df: pd.DataFrame) -> pd.DataFrame:
    """
    정규화, 표준화 https://bskyvision.com/849
    :return: 표준화
    """
    df["Price"] = pd.to_numeric(df["Price"])
    mean, std = df.mean(axis=0), df.std(axis=0)
    return (df["Price"] - mean["Price"]) / std["Price"]


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """
    정규화, 표준화 https://bskyvision.com/849
    :return: 정규화
    :rtype:
    """
    max_v, min_v = df.max(axis=0), df.min(axis=0)
    return (df["Price"] - min_v["Price"]) / (max_v["Price"] - min_v["Price"])
