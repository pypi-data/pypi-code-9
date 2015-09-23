'''collection of routines to support python 2&3 code in this package'''
# std py3k stanza
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import sys


def iteritems(dct):
    '''return the appropriate method'''
    if sys.version_info < (3, ):
        return dct.iteritems()
    else:
        return dct.items()


def py_ver():
    '''return the Major python version, 2 or 3'''
    return sys.version_info[0]

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
