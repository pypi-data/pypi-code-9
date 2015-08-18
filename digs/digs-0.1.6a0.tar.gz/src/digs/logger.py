#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto

from logging import StreamHandler, DEBUG, getLogger as realGetLogger, Formatter
import logging

from colorama import Fore, Back, Style, init
from utils import to_display

init()


class ColourStreamHandler(StreamHandler):

    """ A colorized output SteamHandler """

    # Some basic colour scheme defaults
    colours = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARN': Fore.YELLOW,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRIT': Back.RED + Fore.WHITE,
        'CRITICAL': Back.RED + Fore.WHITE
    }

    def emit(self, record):
        try:
            message = self.format(record)
            try:
                message = to_display(message)
            except Exception:
                pass
            line = Style.RESET_ALL + self.colours[
                record.levelname] + '{} | '.format(record.levelname)

            if record.levelname not in ['CRITICAL', 'CRIT', 'ERROR']:
                line += Style.RESET_ALL

            line += message
            if record.levelname in ['DEBUG', 'CRITICAL', 'CRIT', 'ERROR']:
                line += ' :: {filename} : {lineno}'.format(
                    filename=record.filename, lineno=record.lineno)
            line += Style.RESET_ALL
            self.stream.write(line)
            self.stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


def getLogger(name=None, fmt='%(message)s'):
    log = realGetLogger(name)
    handler = ColourStreamHandler()
    handler.setLevel(DEBUG)
    handler.setFormatter(Formatter(fmt))
    log.addHandler(handler)
    log.setLevel(DEBUG)
    log.propagate = 0  # Don't bubble up to the root logger
    return log


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()


@singleton
class Logger(object):
    level = logging.DEBUG

    def __init__(self, db=None):
        self.log = getLogger('digs')
        if db:
            self.level = db
        self.log.setLevel(self.level)
