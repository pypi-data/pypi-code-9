# -*- coding: utf-8 -*-
__author__ = 'sergey.meerovich'
"""This package is print elements on nested list
"""
def nestlists(listname):
    for item in listname:
        if isinstance(item,list):
            nestlists(item)
        else:
            print item


