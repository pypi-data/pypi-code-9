# -*- coding: utf-8 -*-
#
# getwrapspec: Get argspec of wrapped functions for side-effect-only decorators
# Copyright 2015 Thomas Perl <thp.io>. All rights reserved.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#


"""Get argspec of wrapped functions for side-effect-only decorators"""


__author__ = 'Thomas Perl <m@thp.io>'
__version__ = '1.0.0'
__url__ = 'http://thp.io/2015/getwrapspec/'
__license__ = 'ISC'


import functools
import inspect


def wraps(f):
    """Extended functools.wraps drop-in when parameters don't change

    When the wrapper has the same signature as the wrapped function, and it
    doesn't change the args, use this, so that getwrapspec.getargspec()
    can return the real function's argspec.
    """
    inner_decorator = functools.wraps(f)

    def decorator(func):
        func = inner_decorator(func)
        func._getwrapspec_realfunc = f
        return func

    return decorator


def getargspec(f):
    """Extended inspect.getargspec drop-in that returns the wrapped function's argspec

    For wrapper functions with the same signature (see getwrapspec.wraps()),
    returns the argspec of the real function instead of the wrapper's argspec.
    """
    while hasattr(f, '_getwrapspec_realfunc'):
        f = f._getwrapspec_realfunc
    return inspect.getargspec(f)
