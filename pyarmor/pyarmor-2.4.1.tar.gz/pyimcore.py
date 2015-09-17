# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      Copyright @ 2013 Dashingsoft corp.                   #
#      All rights reserved.                                 #
#                                                           #
#      Pyshield                                             #
#                                                           #
#      Version: 1.7.0 -                                     #
#                                                           #
#############################################################
#
#
#  @File: pyimcore.py
#
#  @Author: Jondy Zhao(jondy.zhao@gmail.com)
#
#  @Create Date: 2011/09/15
#
#  @Description:
#
#   Install an import hook for pyshield
#
import sys
import imp
import os
import site

ext_char = os.getenv('PYARMOR_EXTRA_CHAR', 'e')
ext_list = [ x + ext_char for x in ('.pyc', '.pyo', '.pyd', '.so') ]

try:
    import pytransform
except Exception:
    pass

class PyshieldImporter(object):

    def __init__(self):
        self.filename = ""
        self.modtype = 0

    def find_module(self, fullname, path=None):
        try:
            _name = fullname.rsplit('.', 1)[-1]
        except AttributeError:
            # no rsplit in Python 2.3
            _name = fullname.split('.', 1)[-1]
        if path is None:
            path = sys.path
        for dirname in path:
            self.filename = os.path.join(dirname, _name + '.py' + ext_char)
            if os.path.exists(self.filename):
                self.modtype = 0
                return self
            for ext in ext_list:
                self.filename = os.path.join(dirname, _name + ext)
                if os.path.exists(self.filename):
                    self.modtype = 1 if ext in ext_list[:2] else 2
                    return self
        self.filename = ""

    def load_module(self, fullname):
        ispkg = 0
        try:
            mod = pytransform.import_module(
                fullname,
                self.filename,
                self.modtype
                )
            mod.__file__ = "<%s>" % self.__class__.__name__
            mod.__loader__ = self
        except Exception:
            raise ImportError("error occurred when import module")
        return mod

# install the hook
sys.meta_path.append(PyshieldImporter())
