#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015, RedJack, LLC.
# All rights reserved.
#
# Please see the COPYING file in this distribution for license details.
import ast
import re
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()


_version_re = re.compile(r'__version__\s+=\s+(.*)')


with open('akadata/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='akadata',
    version=version,
    description='Python port of Akamai EdgeScape client',
    long_description=readme,
    author='Andy Freeland',
    author_email='andy.freeland@redjack.com',
    url='https://github.com/redjack/akadata-py',
    packages=find_packages(exclude=['tests']),
    install_requires=[],
    extras_require={
        # Require 'ipaddress' module on Python 2.7
        ':python_version=="2.7"': ['ipaddress'],
    },
    zip_safe=False,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
