#!/usr/bin/env python
"""
KASH API Client
See https://docs.withkash.com for more details
Copyright (c) 2015 Kash Corp. All rights reserved.
Use of this source code is governed by a BSD-style license that can be
found in the LICENSE file.
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

from setuptools import setup

setup(
    name='kash',
    version='0.1.1',
    description='Kash API Python Client',
    author='Kash',
    author_email='developers@withkash.com',
    #need a url
    url='https://bitbucket.org/avidtap/kash_python',
    packages=find_packages(),
    install_requires=['requests']    
)
