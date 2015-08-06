#!/usr/bin/env python

"""Setup script for packaging kabutopy.

Requires setuptools.

To build the setuptools egg use
    python setup.py bdist_egg
and either upload it to the PyPI with:
    python setup.py upload
or upload to your own server and register the release with PyPI:
    python setup.py register

A source distribution (.zip) can be built with
    python setup.py sdist --format=zip

That uses the manifest.in file for data files rather than searching for
them here.

"""

import sys
import os
import warnings

from setuptools import setup, Extension, find_packages
import re

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.rst')) as f:
        README = f.read()
except IOError:
    README = ''


__author__ = 'See AUTHORS'
__license__ = 'MIT/Expat'
__author_email__ = 'maarten@adimian.com'
__maintainer_email__ = __author_email__
__url__ = 'https://hg.adimian.com/products/kabutopy'

def get_version():
    f = open(os.path.join(here, 'kabutopy', '__init__.py'))
    version_file = f.read()
    f.close()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(name='kabutopy',
    packages=find_packages(),
    # metadata
    version=get_version(),
    description="client for the kabuto service",
    long_description=README,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    install_requires=[
        'requests==2.7.0',
        'six'
    ],
    classifiers=[
                 'Development Status :: 4 - Beta',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 ],
    )
