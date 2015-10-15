#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for the Safecast Tracker.

Source:: https://github.com/ampledata/safecast_tracker
"""


__title__ = 'safecast_tracker'
__version__ = '1.0.0'
__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.co>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2015 Orion Labs, Inc.'


import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # pylint: disable=F0401,E0611


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist upload')
        sys.exit()


publish()


setup(
    name='safecast_tracker',
    version=__version__,
    description='Safecast Tracker for APRS.',
    author='Greg Albrecht',
    author_email='gba@orionlabs.co',
    packages=['safecast_tracker'],
    package_data={'': ['LICENSE']},
    license=open('LICENSE').read(),
    long_description=open('README.rst').read(),
    url='https://github.com/ampledata/safecast_tracker',
    setup_requires=[
      'coverage >= 3.7.1',
      'nose >= 1.3.7'
    ],
    install_requires=[
        'aprs >= 4.0.0',
        'pygatt',
        'pynmea2 >= 1.4.2',
        'pyserial >= 2.7',
    ],
    package_dir={'safecast_tracker': 'safecast_tracker'},
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'safecast_tracker = safecast_tracker.cmd:sc_tracker'
        ],
    }
)
