#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# xwot_dsl.py - Python _dsl for the xwot meta model.
# Copyright (C) 2015  Lars Vögtlin
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

__author__ = 'Lars Voegtlin'

from setuptools import setup, find_packages

VERSION = "1.0.0"

setup(
    name="xwot_dsl",
    packages=find_packages('.', exclude=["test", "_dsl._old_grammar"]),
    version=VERSION,
    install_requires=['pyparsing==2.0.1'],
    description="xwot_dsl",
    author="Lars Voegtlin",
    author_email="lvoegtlin@gmail.com",
    license="GPLv3",
    classifiers=['License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
    ext_modules=[],
    long_description="""\
xwot_dsl.py
-------------------------------------
xwot_dsl.py - Python _dsl for the xwot meta model.
"""
)