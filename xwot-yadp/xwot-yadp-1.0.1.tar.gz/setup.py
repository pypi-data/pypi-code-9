#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Yadp  - Yet Another Discovery Protocol
# Copyright (C) 2015  Alexander Rüedlinger
#
# This file is part of Yadp.
#
# Yadp is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Yadp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Yadp.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Alexander Rüedlinger'

import os
import glob
from setuptools import setup, find_packages

VERSION = "1.0.1"
data_dir = os.path.join('frontend', 'public')
data_files = [(data_dir, [f for f in glob.glob(os.path.join(data_dir, '*'))])]

setup(
    name="xwot-yadp",
    packages=find_packages(exclude=['test']),
    version=VERSION,
    entry_points={
        'console_scripts': [
            'yadp = yadp.cmd:yadp_listener',
            'semantic-yadp = yadp.cmd:semantic_yadp_listener',
            'web-yadp = yadp.cmd:web_yadp'
        ]
    },
    install_requires=['twisted>=15.2', 'klein>=15.0', 'treq>=0.2',
                      'rdflib>=4.2', 'rdfextras>=0.4', 'rdflib-jsonld>=0.3',
                      'xmltodict>=0.9.2', 'stemming==1.0'],
    data_files=data_files,
    description="Yet Another Discovery Protocol",
    author="Alexander Rüedlinger",
    author_email="a.rueedlinger@gmail.com",
    url="https://github.com/lexruee/yadp",
    license="AGPL v3",
    classifiers=['License :: OSI Approved :: GNU Affero General Public License v3'],
    py_modules=[""],
    long_description="""\
Yadp - Yet Another Discovery Protocol
-------------------------------------
Yadp is a prototype implementation of a Discovery Protocol.

   1) It allows to carry user-defined payload data.
   2) It's line oriented protocol and looks like HTTP.
   3) It allows to carry meta headers to encode the content-type of the user-defined payload data,
      a location header to retrieve more information about the discovered service.

"""
)
