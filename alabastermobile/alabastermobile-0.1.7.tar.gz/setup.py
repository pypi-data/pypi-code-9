#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
from setuptools import setup, find_packages

import alabastermobile


# README into long description
with codecs.open('README.md', encoding='utf-8') as f:
    readme = f.read()
# REQUIREMENTS
with open('REQUIREMENTS.txt') as f:
    required = f.read().splitlines()

setup(
    name='alabastermobile',
    version=alabastermobile.__version__,
    packages=find_packages(),
    author="Frederic Aoustin",
    author_email="fraoustin@gmail.com",
    description="theme for ablog",
    long_description= readme,
    include_package_data=True, #use manifest.ini
    install_requires=required,
    url='https://github.com/fraoustin/alabastermobile',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Documentation",
    ],

)
