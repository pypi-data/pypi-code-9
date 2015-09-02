# encoding=utf-8

import logging

from configs import config


logger = logging.getLogger(None)
logger.setLevel(logging.INFO)


def add_handler(logger, handler):
    formatter = logging.Formatter(
        '%(asctime)s,%(name)s,%(levelname)s: %(message)s'
    )

    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)


if config.logfile:
    add_handler(logger, logging.FileHandler(config.logfile))
