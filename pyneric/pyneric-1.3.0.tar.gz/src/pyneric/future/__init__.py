# -*- coding: utf-8 -*-
"""pyneric.future module

This is equivalent to future.builtins with additions and customizations.

"""
# flake8: noqa

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys

from future.builtins import *
from future.builtins import __all__ as _all


_all = set(_all)

_all.add('future')
from future import utils as future

# PY2 note: Remove the basestring import and replace 'basestring' with 'str' in
# code when removing Python 2 support.
_all.add('basestring')
from past.builtins import basestring

if future.PY2:
    # Purposely allow Python 2.6 to use this package, rather than:
    #_all |= {'str', 'super', 'type'}
    _all |= set(('str', 'super', 'type'))
    from pyneric.future.newstr import newstr as str
    from pyneric.future.newsuper import newsuper as super
    from pyneric.future.newtype import newtype as type


_all.add('python_2_unicode_compatible')
python_2_unicode_compatible = future.python_2_unicode_compatible
python_2_unicode_compatible.__doc__ = """
    DEPRECATED:  Use this method from its source (`future.utils`).
    With ``from pyneric.future import *``, it can be referenced with
    ``future.python_2_unicode_compatible``."""


_all.add('ensure_text')
def ensure_text(value, encoding=sys.getdefaultencoding(), errors='strict',
                coerce=False):
    """Return the text representation of the given string.

    :param value bytes/str/unicode: string value
    :param encoding str: name of encoding used if `value` is not text
    :param errors str: decode option used if `value` is not text
    :param bool coerce: whether to attempt to coerce `value` to text
    :returns: text representation of `value`
    :rtype: `unicode` if Python 2; otherwise, `str`
    :raises TypeError: if `value` is not a str, unicode, nor bytes
    :raises UnicodeDecodeError: if `value` cannot be decoded

    The primary use case for this function is as a shortcut for a
    library providing support for Python 2 and 3 to ensure that a
    provided string value can be interpreted as text.

    """
    if isinstance(value, future.native_bytes):
        value = value.decode(encoding, errors)
    elif not isinstance(value, future.text_type):
        if not coerce:
            raise TypeError("{!r} is not a string type.".format(type(value)))
        value = future.text_type(value)
    return future.native(value)


__all__ = list(future.native_str(x) for x in _all)
