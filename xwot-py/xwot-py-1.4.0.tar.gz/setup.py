#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# xwot.py - Python tools for the extended Web of Things
# Copyright (C) 2015  Alexander Rüedlinger
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

__author__ = 'Alexander Rüedlinger'

from setuptools import setup, find_packages

VERSION = "1.4.0"

setup(
    name="xwot-py",
    packages=find_packages('.', exclude=["tests", "test"]),
    entry_points={
        'console_scripts': [
            'xwotc = xwot.cmd:xwotc',
            'xwotd = xwot.cmd:xwotd'
        ]
    },
    version=VERSION,
    install_requires=['dicttoxml==1.6.6', 'xmltodict==0.9.2'],
    description="xwot",
    author="Alexander Rüedlinger",
    author_email="a.rueedlinger@gmail.com",
    license="GPLv3",
    classifiers=['License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
    ext_modules=[],
    long_description="""\
xwot.py
-------------------------------------

xwot.py - Python tools for the extended Web of Things

"""
)
