import logging

_console_log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(
    format=_console_log_format,
    level=logging.DEBUG
)


def get_logger(name):
    return logging.getLogger(__name__)
