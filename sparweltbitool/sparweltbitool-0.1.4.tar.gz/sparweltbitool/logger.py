import os
import logging
from sparweltbitool.config import config

class Logger(object):
    """Configuration for logging."""

    def __init__(self, identifier=None):

        logger_identifier = identifier if identifier is not None else config.get('logger', 'default_identifier')

        self.logger = logging.getLogger(logger_identifier)
        logging.basicConfig(
            filename=os.getcwd() + os.path.normpath(config.get('logger', 'log_file')),
            level=config.get('logger', 'log_level'),
            format='[%(asctime)-15s] {}.%(levelname)s: %(message)s'.format(config.get('logger', 'app_name')),
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def error(self, msg):
        logging.error(msg)

    def warning(self, msg):
        logging.warning(msg)

    def info(self, msg):
        logging.info(msg)

    def debug(self, msg):
        logging.debug(msg)
