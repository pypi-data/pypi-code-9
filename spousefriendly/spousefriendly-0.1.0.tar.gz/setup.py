#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'easygui>=0.97.4',
]

if sys.version_info < (3, 4):
    requirements.append('enum34')

test_requirements = [
    'mock>=1.3',
]

setup(
    name='spousefriendly',
    version='0.1.0',
    description="Be nice to your spouse - give your command line scripts some GUI feedback when needed.",
    long_description=readme + '\n\n' + history,
    author="Luke Plant",
    author_email='L.Plant.98@cantab.net',
    url='https://bitbucket.com/spookylukey/spousefriendly',
    packages=[
        'spousefriendly',
    ],
    package_dir={'spousefriendly':
                 'spousefriendly'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='spousefriendly',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
