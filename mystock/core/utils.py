import logging
import math
from decimal import Decimal


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


log = MyLogger()


def check_nan_return_or_zero(value) -> Decimal:
    if math.isnan(value):
        return Decimal("0")
    else:
        return Decimal(value)
