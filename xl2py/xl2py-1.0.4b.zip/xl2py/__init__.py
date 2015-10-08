# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function

__author__ = {'Gabriel S. Gusmao' : 'gusmaogabriels@gmail.com'}
__version__ = '1.0.4b'

"""

By Gabriel S. Gusmão (Gabriel Sabença Gusmão)
May, 2015

    xl2Py version 1.0.4b alpha

    ~~~~

    "An Excel 2 Python I/O Structure reShaping"

    :copyright: (c) 2015 Gabriel S. Gusmão
    :license: MIT, see LICENSE for more details.

"""

from .core import processor
from .core.xlref_base import xlref
from .core.constructor import builder

__all__ = ['processor','builder','xlref','__author__','__version__']
