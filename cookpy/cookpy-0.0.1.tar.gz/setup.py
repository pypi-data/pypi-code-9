#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from setuptools import setup

import cookpy

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    long_description = readme.read()

setup(
    name='cookpy',
    version=cookpy.version,
    description='A cross-platform, free and open-source build system',
    long_description=long_description,
    url='https://github.com/cookpy/cookpy',
    author='koehlja',
    packages=['cookpy'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools'],
    keywords=[
        'cookpy', 'cook', 'py', 'build', 'system', 'tools'])
