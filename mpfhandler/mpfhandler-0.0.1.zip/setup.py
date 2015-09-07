#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This is the module's setup script.  To install this module, run:
#
#   python setup.py install
#
import sys

from setuptools import setup, find_packages


VERSION = "0.0.1"
classifiers = """\
Development Status :: 4 - Beta
Topic :: System :: Logging
Operating System :: POSIX
Programming Language :: Python
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Topic :: Software Development :: Libraries :: Python Modules
License :: OSI Approved :: Apache Software License
"""
with open('README.rst', 'r') as f:
    doc = f.read()



setup(name='mpfhandler',
      version=VERSION,
      author="yorks",
      author_email="stuyorks@gmail.com",
      package_dir={ '' : 'src', },
      py_modules=['mpfhandler'],
      #packages=['src'],
      #data_files=[
      #  ('docs', [
      #      'README.rst',
      #      'LICENSE',
      #      ]),
      #],
      url="https://github.com/yorks/mpfhandler",
      download_url = 'https://github.com/yorks/mpfhandler/releases/tag/'+VERSION,
      license = "http://www.apache.org/licenses/LICENSE-2.0",
      description='a timed rotate logging file handler, support multiple processes (base logging.RotatingFileHandler, portalocker)',
      long_description=doc+'\n\n',
      platforms = [ "nt", "posix" ],
      keywords = "logging, linux, unix, rotate, portalocker, django, mutiple processes",
      classifiers=classifiers.splitlines(),
      install_requires=['portalocker'],
      #test_suite=unittest.TestSuite,
)
