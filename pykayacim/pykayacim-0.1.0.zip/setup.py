#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
from setuptools import setup
import pykayacim

# Loads README.rst and HISTORY.rst
DESCRIPTION_DOCUMENTS = ["README.rst", "HISTORY.rst"]
long_description = ""
for doc in DESCRIPTION_DOCUMENTS:
    with open(doc, "r") as f_doc:
        long_description += f_doc.read()

# PyPI classifiers
CLASSIFIERS = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Utilities"
    ]

# PyPI keywords
KEYWORDS = [
    "im.kayac.com", "notification", "Kayac", "push",
    "iPhone", "Jabbler"]

ENTRY_POINTS = {
    "console_scripts": ["ezkayacim = pykayacim.ezkayacim:main"]}

setup_args = {
    "name": "pykayacim",
    "version": pykayacim.__version__,
    "author": pykayacim.__author__,
    "author_email": "hamukichi-dev@outlook.jp",
    "url": "https://github.com/hamukichi/pykayacim",
    "description": "Send push notifications via im.kayac.com.",
    "long_description": long_description,
    "packages": ["pykayacim"],
    "classifiers": CLASSIFIERS,
    "provides": ["pykayacim"],
    "license": pykayacim.__license__,
    "keywords": KEYWORDS,
    "install_requires": ["future"],
    "entry_points": ENTRY_POINTS
    }

setup(**setup_args)