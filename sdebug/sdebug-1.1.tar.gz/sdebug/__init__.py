# -*- coding: utf-8 -*-
#    Copyright (C) 2015 by
#    Moreno Bonaventura <morenobonaventura@gmail.com>
#    This is Free Software - You can use and distribute it under
#    the terms of the GNU General Public License, version 3 or later.
"""
simple debug
"""
__author__   = 'Moreno Bonaventura <morenobonaventura@gmail.com>'

import sys

if sys.version_info[:2] < (2, 6):
    m = "Python version 2.6 or later is required for simple_debug (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys

from sdebug import *
