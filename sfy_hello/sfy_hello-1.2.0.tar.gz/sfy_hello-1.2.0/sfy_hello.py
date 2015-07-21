# -*- coding: UTF-8 -*-
from __future__ import print_function
from distutils.core import setup
setup(
        name    = 'sfy_hello',
        version = '1.2.0',
        # py_modules = ['sfy_hello'],
        author  = 'sfy',
        author_email = '111',
        url     = 'sssss',
        description = 'aaaaa'
        
        )
# 试试可以不可以用汉字
# this is my commen
def print_lol(m_list,tag = False, level=0):
        for item in m_list:
                     if isinstance(item, list):
                            print_lol(item, level+1)
                     else:
                         if tag== True:
                             for tab in range(level):
                                print('\t', end='')
                         print(item)
