# -*- coding: UTF-8 -*-

"""
Builds a *context* from arguments and renders one or more Jinja *templates* with
it. You can build the context by manually setting keywords, loading data files
or giving content as markup files.

"""

from __future__ import absolute_import
from __future__ import unicode_literals


__VERSION__ = '0.6.0'
__author__ = 'Brutus [DMC] <brutus.dmc@googlemail.com>'
__license__ = 'GNU General Public License v3 or above - '\
              'http://www.opensource.org/licenses/gpl-3.0.html'


from .__main__ import render
