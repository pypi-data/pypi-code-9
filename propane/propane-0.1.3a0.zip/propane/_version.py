# coding=utf-8
import time
from datetime import date

from propane.distribution import version_class

# This file is originally generated from Git information by running 'setup.py
# version'. Distribution tarballs contain a pre-generated copy of this file.

__version__ = '0.1.3alpha'
__date__ = date(2015, 7, 27)
__time__ = time.gmtime(1438041714.5)

version = version_class(__version__, __date__, __time__)
