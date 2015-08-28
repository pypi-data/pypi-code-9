#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Based on https://github.com/pypa/sampleproject/blob/master/setup.py."""
from __future__ import unicode_literals
# To use a consistent encoding
import codecs
import os
from setuptools import setup, find_packages
import sys


def parse_readme():
    """Parse contents of the README."""
    # Get the long description from the relevant file
    here = os.path.abspath(os.path.dirname(__file__))
    readme_path = os.path.join(here, 'README.md')
    with codecs.open(readme_path, encoding='utf-8') as handle:
        long_description = handle.read()

    return long_description


setup(
    name='youtux.test-travis',

    # Versions should comply with PEP440. For a discussion on
    # single-sourcing the version across setup.py and the project code,
    # see http://packaging.python.org/en/latest/tutorial.html#version
    version='1.2.0-beta',

    description='Vanguard contains all the boilerplate you need to bootstrap a modern Python package.',
    long_description=parse_readme(),
    # What does your project relate to? Separate with spaces.
    keywords='test-travis development',
    author='Alessio Bogon',
    author_email='youtux@example.com',
    license='MIT',

    # The project's main homepage
    url='https://github.com/youtux/test-travis',

    packages=find_packages(exclude=('tests*', 'docs', 'examples')),

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    include_package_data=True,
    zip_safe=False,

    # Install requirements loaded from ``requirements.txt``
    install_requires=['six'],

    test_suite='tests',

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and
    # allow pip to create the appropriate form of executable for the
    # target platform.
    entry_points=dict(
        console_scripts=[
            'test-travis = test_travis.__main__:cli',
        ],
    ),

    # See: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are:
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

        'Environment :: Console',
    ],
)
