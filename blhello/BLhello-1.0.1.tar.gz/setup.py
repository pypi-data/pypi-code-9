#!/usr/bin/env python

import codecs
import os
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup

def read(fname):
	return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = "BLhello"

PACKAGES = ["BLhello",]

KEYWORDS = "test python package"

LONG_DESCRIPTION = read("README.txt")

DESCRIPTION = "this is going to say Hello to world!"

AUTHOR = "Joey Chu"

VERSION = "1.0.1"

URL = "https://github.com/joeychu1986/web_app"

LICENSE = "MIT"

AUTHOR_EMAIL = "cqtcwr@gmail.com"

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)
 

