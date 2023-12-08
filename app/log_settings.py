import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger(log_file: str, logger_name: str, level=logging.INFO):
    """
    :param log_file: path to a file with a .log extension, where the logs of this handler will be sent.
    :param logger_name: unique name for the logger handler.
    :param level: (default=logging.INFO) if necessary, you can specify a specific logging level for individual handler.
    :return: logger
    """
    os.makedirs("logs", exist_ok=True)  # Creates a directory for logs when creating a database

    logger = logging.getLogger(logger_name)  # use unique logger per file
    logger.setLevel(level)

    handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)  # if full, a new file will be created
    handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)

    if not logger.hasHandlers():  # Checks if the logger has any handlers already installed
        logger.addHandler(handler)

    return logger
