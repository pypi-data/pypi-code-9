# -*- coding: utf-8  -*-
"""A setuptools based setup module."""

from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='competitions-match',
    version='0.1.2',

    description='competitions support library for matches',
    long_description=long_description,

    url='https://github.com/happy5214/competitions-match',

    author='Alexander Jones',
    author_email='happy5214@gmail.com',

    license='LGPLv3+',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='competitions matches',

    packages=find_packages(exclude=['docs', 'tests*']),

    namespace_packages=['competitions'],

    test_suite='tests',

    entry_points={
        'competitions.match.base': [
            'competitions.simple = competitions.match.default.SimpleMatch:SimpleMatch',
            'competitions.test = competitions.match.default.TestMatch:TestMatch'
        ]
    },
)
