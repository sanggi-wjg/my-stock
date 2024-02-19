import logging

from django.utils import timezone


class MyLogger:
    def __init__(self):
        formatter = logging.Formatter(
            "[%(levelname)s] [%(asctime)s] [%(pathname)s:%(lineno)d]\t %(message)s",
            datefmt="%Y-%m-%d %I:%M:%S",
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        self.debug_logger = logging.getLogger("logger.debug")
        self.debug_logger.setLevel(logging.DEBUG)
        self.debug_logger.addHandler(stream_handler)

        self.info_logger = logging.getLogger("logger.info")
        self.info_logger.setLevel(logging.INFO)
        self.info_logger.addHandler(stream_handler)

        self.warn_logger = logging.getLogger("logger.warn")
        self.warn_logger.setLevel(logging.WARNING)
        self.warn_logger.addHandler(stream_handler)

        self.error_logger = logging.getLogger("logger.error")
        self.error_logger.setLevel(logging.ERROR)
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


def get_now_text(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    return timezone.now().strftime(date_format)
