#!/usr/bin/env python

import sys
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (2,5):
    raise NotImplementedError("Sorry, you need at least Python 2.5 or Python 3.x to use youtube_me.")

import youtube_me

setup(name='youtube_me',
      version=youtube_me.__ver__,
      description='Automatic YouTube downloading...',
      author=youtube_me.__author__,
      author_email='jmilne@graphic-designer.com',
      py_modules=['youtube_me'],
      scripts=['youtube_me.py'],
      install_requires=["youtube-dl"],
      license='Public Domain',
      platforms = 'any',
      classifiers=['Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ]
      )
