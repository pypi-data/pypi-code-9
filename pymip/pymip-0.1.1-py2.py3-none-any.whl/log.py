# -*- coding: utf-8 -*-
from datetime import date
import logging
import os.path

LEVELS = {0: 'ERROR', 1: 'WARNING', 2: 'INFO', 3: 'DEBUG'}
TEMPLATE = "[%(asctime)s] %(name)-25s %(levelname)-8s %(message)s"
FORMATTER = logging.Formatter(TEMPLATE)


def setup_daily_logging(log_dir, level='INFO'):
    """Setup logging using ``FileHandler`` based on current date."""
    # use isoformatted date as filename: "2015-11-14"
    today = date.today().isoformat()
    filename = os.path.join(log_dir, "{}.log".format(today))

    # setup handler that will rotate daily
    daily_handler = logging.FileHandler(filename)

    # configure handler
    daily_handler.setFormatter(FORMATTER)
    daily_handler.setLevel(level)

    return daily_handler


def setup_stream_logging(level='ERROR'):
    """Setup logging to STDERR."""
    # add a handler to the logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(FORMATTER)

    return console_handler


def setup_logging(filename, file_level='INFO', stderr_level='ERROR',
                  root_level='DEBUG'):
    """Configure central logging for the package."""
    # get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(root_level)

    # setup stream logging to STDERR
    console = setup_stream_logging(level=stderr_level)
    file_handler = setup_daily_logging(filename, level=file_level)

    root_logger.addHandler(console)
    root_logger.addHandler(file_handler)
    return root_logger
