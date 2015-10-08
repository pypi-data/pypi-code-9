# coding=utf8

"""
:mod:`ulib` is a library for processing the unicode character or string more pythonic.

.. warning:: This module not finished, don't use it on product environment.

Support:

    * Chinese
"""

from . import (
    ToolkitException,
    text_type,
    logger,
    PY2
)

if not PY2:
    unichr = chr


class ULibException(ToolkitException):
    pass


class NotUnicodeException(ULibException):
    pass


def _is(u, start, end):
    try:
        oridinal = ord(u)
    except TypeError:
        err_msg = 'ulib excepted an unicode character, but {} of length {} found'
        raise NotUnicodeException(err_msg.format(type(u), len(u)))
    else:
        return True if start <= oridinal <= end else False


def is_cn(u):
    """
    Test if the unicode character is a chinese character.

    :param u: Unicode character.
    :return: Bool Value
    """
    return _is(u, 0x4e00, 0x9fa5)


def has_cn(us):
    """
    Test if the unicode string contain an unicode chinese character.

    :param us: Unicode string.
    :return: Bool Value
    """
    for u in us:
        if is_cn(u):
            return True
    else:
        return False


def is_digital(u):
    """
    Test if the unicode character is a digital.

    :param u: Unicode character.
    :return: Bool Value
    """
    return _is(u, 0x0030, 0x0039)


def cnlen(us):
    """
    Calculate the length of unicode string. length of chinese character is 2.

    :param us: Unicode string.
    :return: Bool Value
    """
    return len(us) + len(filter(is_cn, us))


def _f2h(u):
    ordinal = ord(u)
    if ordinal == 0x3000:
        ordinal = 0x0020
    elif ordinal == 0x3001:
        ordinal = 0x002c
    elif ordinal == 0x3002:
        ordinal = 0x002e
    else:
        ordinal -= 0xfee0
        print(u)
        print(ordinal)

    if ordinal < 0x0020 or 0x7e < ordinal:
        return u
    return unichr(ordinal)


def f2h(u):
    """

    :param us: Unicode character or string.
    :return:
    """
    if not type(u) is text_type:
        raise NotUnicodeException("f2h() excepted an unicode character or string.")
    if len(u) == 1:
        return _f2h(u)
    else:
        return ''.join(map(_f2h, u))
