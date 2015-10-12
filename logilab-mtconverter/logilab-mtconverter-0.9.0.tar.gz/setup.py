#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0404,W0622,W0704,W0613
# copyright 2003-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-mtconverter.
#
# logilab-mtconverter is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License, or (at your
# option) any later version.
#
# logilab-mtconverter is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-mtconverter. If not, see <http://www.gnu.org/licenses/>.
"""Generic Setup script, takes package info from __pkginfo__.py file.
"""
__docformat__ = "restructuredtext en"

import os
import sys
import shutil
from os.path import isdir, exists, join, dirname, abspath

from setuptools import setup, find_packages

here = abspath(dirname(__file__))

# import optional features
pkginfo = {}
with open(join(here, '__pkginfo__.py')) as f:
    exec(f.read(), pkginfo)

# import required features
modname = pkginfo['modname']
version = pkginfo['version']
license = pkginfo['license']
description = pkginfo['description']
web = pkginfo['web']
author = pkginfo['author']
author_email = pkginfo['author_email']

distname = pkginfo.get('distname', modname)
data_files = pkginfo.get('data_files', None)
subpackage_of = pkginfo.get('subpackage_of', None)
include_dirs = pkginfo.get('include_dirs', [])
ext_modules = pkginfo.get('ext_modules', None)
install_requires = pkginfo.get('install_requires', None)
dependency_links = pkginfo.get('dependency_links', [])

STD_BLACKLIST = ('CVS', '.svn', '.hg', 'debian', 'dist', 'build')

IGNORED_EXTENSIONS = ('.pyc', '.pyo', '.elc', '~')

if exists(join(here, 'README')):
    long_description = open(join(here, 'README')).read()
else:
    long_description = ''

def install(**kwargs):
    """setup entry point"""
    return setup(name = distname,
                 version = version,
                 license = license,
                 description = description,
                 long_description = long_description,
                 author = author,
                 author_email = author_email,
                 url = web,
                 packages = find_packages(exclude=['test*']),
                 data_files = data_files,
                 ext_modules = ext_modules,
                 namespace_packages = [subpackage_of],
                 install_requires = install_requires,
                 **kwargs
                 )

if __name__ == '__main__' :
    install()
