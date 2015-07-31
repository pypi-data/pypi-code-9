# -*- coding: UTF-8 -*-

"""Common classes / functions"""

# System imports
import logging
import siphashc

# Project imports
import syrpc.constants as const


class EmptyException(Exception):
    """Timeout was reached before the server sent an answer"""
    pass


class QueueNotFoundException(Exception):
    """The requested queue does not exist"""
    pass


def _setup_logger():  # pragma: no cover
    """Sets up a default logger"""
    _root = logging.getLogger()
    _lg = _root.getChild(const.General.APP_NAME)
    return _lg


def get_hash(string, queue_count=const.AMQ.NUM_QUEUES):
    """Generates a hash for given string"""
    # Only use the last 31 bits of the 64-bit hash because of serious
    # PHP-retardedness
    hash32 = siphashc.siphash(const.AMQ.HASH, string) & 0x7FFFFFFF  # pylint: disable=no-member
    return hash32 % queue_count


def consts_to_dict(object_):  # pragma: no cover
    """Converts a constants object to a dictionary"""
    new = {}
    for const_ in dir(object_):
        if not const_.startswith("_"):
            new[getattr(object_, const_)] = const_
    return new


lg = _setup_logger()
