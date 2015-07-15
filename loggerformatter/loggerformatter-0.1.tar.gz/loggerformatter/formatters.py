# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from logging import Formatter


class NewFormatter(Formatter):
    """
    Formatter in order to use the format method as in:
    https://docs.python.org/2.7/library/stdtypes.html?highlight=format#str.format
    https://docs.python.org/3.5/library/stdtypes.html?highlight=format#str.format
    """
    def format(self, record):
        """
        Format the LogRecord to a string.
        """
        return record.msg.format(*record.args, **record.__dict__)
