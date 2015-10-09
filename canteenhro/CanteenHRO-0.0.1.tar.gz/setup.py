#!/usr/bin/env python

from distutils.core import setup
from CanteenHRO import CanteenHRO

setup(name='CanteenHRO',
      version=CanteenHRO.__version__,
      description=CanteenHRO.__description__,
      author=CanteenHRO.__author__,
      author_email=CanteenHRO.__author_email__,
      url='https://github.com/mperlet/CanteenHRO',
      packages=['CanteenHRO'],
      keywords = ['Rostock', 'Canteen', 'Mensa'],
     )
