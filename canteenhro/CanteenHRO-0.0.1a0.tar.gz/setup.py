#!/usr/bin/env python

from setuptools import setup
from CanteenHRO.CanteenHRO import CanteenHRO

setup(name='CanteenHRO',
      install_requires=['pyquery==1.2.9'],
      version=CanteenHRO.__version__,
      description=CanteenHRO.__description__,
      author=CanteenHRO.__author__,
      author_email=CanteenHRO.__author_email__,
      url='https://github.com/mperlet/CanteenHRO',
      packages=['CanteenHRO'],
      keywords = ['Rostock', 'Canteen', 'Mensa'],

     )
