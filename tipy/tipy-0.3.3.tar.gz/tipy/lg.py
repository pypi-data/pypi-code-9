#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A class to format the log messages + the logger instance."""

from logging import Formatter, StreamHandler, getLogger, DEBUG


CNRM = '\x1B[0m'
CBLK = '\x1B[30m'
CRED = '\x1B[31m'
CGRN = '\x1B[32m'
CYEL = '\x1B[33m'
CBLU = '\x1B[34m'
CMAG = '\x1B[35m'
CCYN = '\x1B[36m'
CWHT = '\x1B[37m'
BNRM = '\x1B[1m\x1b[00m'
BBLK = '\x1B[1m\x1b[30m'
BRED = '\x1B[1m\x1b[31m'
BGRN = '\x1B[1m\x1b[32m'
BYEL = '\x1B[1m\x1b[33m'
BBLU = '\x1B[1m\x1b[34m'
BMAG = '\x1B[1m\x1b[35m'
BCYN = '\x1B[1m\x1b[36m'
BWHT = '\x1B[1m\x1b[37m'
BOLD = '\x1B[1m'


class ColorFormatter(Formatter):
    """Add color to log messages by overring logging.Formater methods."""

    FORMAT = ("[$BOLD%(filename)-8s: "
              "%(funcName)20s():%(lineno)4s$RESET][%(levelname)-18s] "
              "%(message)s ")
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

    COLOR_SEQ = "\x1B[%dm"

    COLORS = {
        'WARNING': YELLOW,
        'INFO': WHITE,
        'DEBUG': BLUE,
        'CRITICAL': YELLOW,
        'ERROR': RED
    }

    def __init__(self, use_color=True):
        msg = self.formatter_msg(self.FORMAT, use_color)
        Formatter.__init__(self, msg)
        self.use_color = use_color

    def formatter_msg(self, msg, use_color=True):
        if use_color:
            msg = msg.replace("$RESET", CNRM)
            msg = msg.replace("$BOLD", BOLD)
        else:
            msg = msg.replace("$RESET", "")
            msg = msg.replace("$BOLD", "")
        return msg

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in self.COLORS:
            fore_color = 30 + self.COLORS[levelname]
            levelname_color = self.COLOR_SEQ % fore_color + levelname + CNRM
            record.levelname = levelname_color
        return Formatter.format(self, record)


CF = ColorFormatter()
handler = StreamHandler()
handler.setFormatter(CF)
#: The logger which can be used anywhere in the program
lg = getLogger('root')
lg.setLevel(DEBUG)
lg.addHandler(handler)
