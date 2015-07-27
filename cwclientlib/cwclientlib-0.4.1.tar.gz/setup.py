#!/usr/bin/env python
# pylint: disable=W0142,W0403,W0404,W0613,W0622,W0622,W0704,R0904,C0103,E0611
#
# copyright 2003-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of cwclientlib.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <http://www.gnu.org/licenses/>.
"""Generic Setup script, takes package info from __pkginfo__.py file
"""
__docformat__ = "restructuredtext en"

import os
import sys
import shutil
from os.path import isdir, exists, join, dirname

from setuptools import setup, find_packages
from codecs import open


# load metadata from the __pkginfo__.py file so there is no risk of conflict
# see https://packaging.python.org/en/latest/single_source_version.html
base_dir = dirname(__file__)

pkginfo = {}
with open(join(base_dir, "cwclientlib", "__pkginfo__.py")) as f:
    exec(f.read(), pkginfo)
    
# get required metadatas
modname = pkginfo['modname']
version = pkginfo['version']
license = pkginfo['license']
description = pkginfo['description']
web = pkginfo['web']
author = pkginfo['author']
author_email = pkginfo['author_email']
classifiers = pkginfo['classifiers']

with open(join(base_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# get optional metadatas
distname = pkginfo.get('distname', modname)
console_scripts = pkginfo.get('console_scripts', ())
include_dirs = pkginfo.get('include_dirs', ())
data_files = pkginfo.get('data_files')
ext_modules = pkginfo.get('ext_modules')
dependency_links = pkginfo.get('dependency_links', ())
install_requires = pkginfo.get('install_requires')
extras_require = pkginfo.get('extras_require')
test_suite = pkginfo.get('test_suite')

def install(**kwargs):
    """setup entry point"""
    return setup(name=distname,
                 version=version,
                 license=license,
                 description=description,
                 long_description=long_description,
                 author=author,
                 author_email=author_email,
                 url=web,
                 entry_points=dict(console_scripts=console_scripts,),
                 data_files=data_files,
                 include_package_data=True,
                 ext_modules=ext_modules,
                 classifiers=classifiers,
                 packages=find_packages(),
                 install_requires=install_requires,
                 extras_require=extras_require,
                 dependency_links=dependency_links,
		 test_suite=test_suite,
                 **kwargs
                 )

if __name__ == '__main__' :
    install()
