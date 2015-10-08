# coding=utf8

import sys
import logging

logger = logging.getLogger(__name__)

PY2 = sys.version_info[0] == 2

if not PY2:
    iteritems = lambda d: d.items()
    text_type = str
    binary_type = bytes
    long_type = float
    basestring = (str, bytes)
else:
    iteritems = lambda d: d.iteritems()
    text_type = unicode  # noqa
    binary_type = str
    long_type = long  # noqa


class ToolkitException(Exception):
    pass
