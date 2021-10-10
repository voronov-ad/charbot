import logging
from .config import LOGGING_LEVEL
_console_log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(
    format=_console_log_format,
    level=LOGGING_LEVEL
)


def get_logger(name):
    return logging.getLogger(__name__)
