#!/usr/bin/python

# File: setup.py
# Author: Michael Stevens <mstevens@etla.org>
# Copyright (C) 2010

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(name = "beatbox3",
      version = "0.96",
      py_modules = ["beatbox3", "xmltramp2"],
      description = "Makes the salesforce.com SOAP API easily accessible. for Python 3",
      author = "Simon Fell, ported to python3 by Bill Blanchard",
      classifiers = [
        "License :: OSI Approved :: GNU General Public License (GPL)",
		"Intended Audience :: Developers",
        ],
	  url = "http://www.pocketsoap.com/beatbox/",
	  packages = find_packages()
      )
