import logging
import math
from decimal import Decimal
from typing import List, Tuple

from django.utils import timezone


class MyLogger:
    def __init__(self):
        self.debug_logger = logging.getLogger("logger.debug")
        self.info_logger = logging.getLogger("logger.info")
        self.warn_logger = logging.getLogger("logger.warn")
        self.error_logger = logging.getLogger("logger.error")

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
    if math.isnan(value):
        return Decimal("0")
    else:
        return Decimal(value)


def get_now_text(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    return timezone.now().strftime(date_format)


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


def debug_fonts():
    import matplotlib.font_manager as fm

    f = [f.name for f in fm.fontManager.ttflist]
    logger.debug(f)
