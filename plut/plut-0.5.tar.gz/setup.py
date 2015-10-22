#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import plut
from setuptools import setup

setup(name='plut',
      version='0.5',
      description='port manager for developing multiple local web apps',
      long_description=open('readme.rst').read(),
      author='Brandon Hsiao',
      author_email='bh@stoatlabs.com',
      url='https://github.com/brhsiao/plut',
      download_url='https://github.com/brhsiao/plut/tarball/0.5',
      packages=['plut'],
      entry_points={
        'console_scripts': [
          'plut = plut:main',
        ]
      },
      license='MIT'
     )
