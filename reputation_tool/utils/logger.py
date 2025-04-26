
import os
from loguru import logger


def logger_init(log_dir="logs", level="INFO", time_stamp=None):
    """
    :param log_dir: directory in which the log file will be stored
    :param level: logging level
    :param time_stamp:
    """
    if not os.path.exists(log_dir):
        print("Logging directory does not exists")
    log_file = f"stress_test_logs_{time_stamp}.log"
    log_path = os.path.join(log_dir, log_file)

    logger.remove()

    custom_format = "{time:DD_MM_YYYY_HH.mm.ss} | {level} | {message}"

    logger.add(
        log_path,
        format=custom_format,
        level=level,
        enqueue=True,
    )

    return logger

