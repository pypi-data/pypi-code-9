# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import *
def to_unicode(s):
    """
    Receive string s and try to return a utf-8 string.
    """
    try:
        return str(s.decode('cp1252'))
    except (UnicodeDecodeError,TypeError):
        try:
            return str(s.decode('ascii'))
        except (UnicodeDecodeError,TypeError):
            return str(s)
