import os

from loguru import logger
from config import LOG_DIRECTORY


def init_logger(task_name: str, log_directory: str = LOG_DIRECTORY):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory, exist_ok=True)

    logger.add(
        "%s/%s_{time:YYYY-MM-DD}.log" % (log_directory, task_name),
        format="{time} {level} {message}",
        compression="zip",
        rotation="1 day",
        retention="3 days",
        level="INFO",
        diagnose=True,
    )
    # logger.debug(f'{task_name} log directory: {log_directory}')
    return logger
