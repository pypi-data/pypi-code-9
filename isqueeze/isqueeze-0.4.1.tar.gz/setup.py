#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import os
from setuptools import setup, find_packages

import isqueeze
 
setup(
    name='isqueeze',
    version=isqueeze.__version__,
    packages=find_packages(),
    author="FredThx",
    author_email="FredThx@gmail.com",
    description="Une interface pour lecteur squeezeBox sur Rpi",
    long_description=open('README.md').read(),
    install_requires=[],
    include_package_data=True,
    url='',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7"
    ],
    license="WTFPL",

)

try:
	os.mkdir('/opt/isqueeze')
except OSError:
	pass
shutil.copy('myisqueeze.py', '/opt/isqueeze/')