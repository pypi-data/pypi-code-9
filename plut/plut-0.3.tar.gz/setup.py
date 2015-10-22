#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import plut

from setuptools import setup

with open('readme.md') as f:
    desc = f.read()

setup(name='plut',
      version='0.3',
      description='port manager for developing multiple local web apps',
      long_description=desc,
      author='Brandon Hsiao',
      author_email='bh@stoatlabs.com',
      url='https://github.com/brhsiao/plut',
      download_url='https://github.com/brhsiao/plut/tarball/0.3',
      packages=['plut'],
      entry_points={
        'console_scripts': [
          'plut = plut:main',
        ]
      },
      license='MIT'
     )
