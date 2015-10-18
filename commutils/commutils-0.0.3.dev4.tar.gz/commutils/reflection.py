#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os,sys


from os.path import dirname,basename

def module_name(__file__):
    return basename(dirname(__file__))



def get_script_name(__file__):
    # return os.path.basename(sys.argv[0])
    return os.path.split(os.path.realpath(__file__))[1]

def get_script_location(__file__):
    "必须在当前文件中, 如果是从外面import进来, 则返回的是import的那个脚本的路径"
    return os.path.split(os.path.realpath(__file__))[0]

def echo_methods(self):
    """ 输出类中所有的方法，以及doc 文档 """
    print("\n Method List: ")
    for attrName in dir(self):
        attr = getattr(self,attrName)
        if callable(attr):
            print(attrName,"():",attr.__doc__)

def echo_attributes(self):
    print("\n Attributes")
    for name in dir(self):
        attr = getattr(self,attr)
        if not callable(attr):
            print(name,":",attr)
