# coding: utf-8

from __future__ import print_function

import struct
import os
from collections import namedtuple

__all__ = ['get_terminal_size']

terminal_size = namedtuple("terminal_size", "columns lines")

def get_terminal_size(fallback=(80, 24)):
    # Unix
    import sys
    import fcntl
    import termios

    try:
        c, l = struct.unpack(
            'hh',
            fcntl.ioctl(sys.__stdout__.fileno(), termios.TIOCGWINSZ, b"\x00\x00\x00\x00")
        )
    except:
        c = fallback[0]
        l = fallback[1]

    return terminal_size(c, l)
