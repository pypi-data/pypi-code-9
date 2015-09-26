""" A nice logging function for me

import logging
from lagerlogger import LagerLogger 
logger = LagerLogger("mymodule")
logger.console(logging.INFO)

"""

import logging
import logging.handlers
import os

FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG


class LagerLogger(logging.Logger):
    """ King of Loggers """
    def __init__(self, name, level=None):
        logging.Logger.__init__(self, name, self.__level(level))
        self.formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")

    def __level(self, lvl):
        return lvl if lvl is not None else logging.DEBUG

    def console(self, level):
        """ adds a console handler """
        ch = logging.StreamHandler()
        ch.setLevel(self.__level(level))
        ch.setFormatter(self.formatter)
        self.addHandler(ch)

    def logfile(self, level, path=None):
        if path is None:
            path = "log.log"
        path = os.path.normpath(os.path.expanduser(path))
        try:
            # Attempt to set up the logger with specified log target
            open(path, "a").close()
            hdlr = logging.handlers.RotatingFileHandler(path, maxBytes=500000, backupCount=5)
            hdlr.setLevel(self.__level(level))
            hdlr.setFormatter(self.formatter)
        except IOError:
            logging.error('Failed to open file %s for logging' % logpath, exc_info=True)
            sys.exit(1)
        self.addHandler(hdlr)

