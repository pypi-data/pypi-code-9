import logging
import sys


def logger():
    return logging.getLogger('simpress')


def setup(name='simpress', format='%(asctime)s [%(levelname)s] %(message)s'):
    logger_ = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(format, '%Y-%m-%d %H:%M:%S'))
    logger_.addHandler(handler)
    logger_.setLevel(logging.INFO)
