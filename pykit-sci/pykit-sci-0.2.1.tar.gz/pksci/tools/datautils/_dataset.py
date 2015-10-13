# -*- coding: utf-8 -*-
"""
===============================================================================
Classes for parsing data sets (:mod:`pksci.tools.datautils._dataset`)
===============================================================================

.. currentmodule:: pksci.tools.datautils._dataset

"""
from __future__ import division, print_function, absolute_import
from __future__ import unicode_literals
from builtins import object

__docformat__ = 'restructuredtext'

__all__ = ['DataSet', 'DataGroup']


class DataSet(object):
    """Class for containing data."""

    def __init__(self):
        self.axhline = self.axvline = None
        self.dataformat = None
        self.fname = None
        self.path = None
        self.fields = None
        self.headers = None
        self.data = None
        self.xdata = None
        self.ydata = None
        self.y2data = None

    def __str__(self):
        strrep = 'DataSet:'
        for k, v in self.__dict__.items():
            strrep += '\n{}={}'.format(k, v)
        return strrep

    def __repr__(self):
        return "<DataSet()>"


class DataGroup(DataSet):
    """Class for containing multiple DataSets"""

    def __init__(self):
        self.groupid = None
