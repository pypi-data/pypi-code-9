#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

from setuptools import setup
from setuptools import find_packages


__version__ = '0.1.2'


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
    'django-extensions',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='django-fabtasks',
    version=__version__,
    description="Common Fabric tasks for use in Django development/deployments",
    long_description=readme + '\n\n' + history,
    author="Tim Santor",
    author_email='tsantor@xstudios.agency',
    url='https://bitbucket.org/tsantor/django-fabtasks',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    keywords='django-fabtasks',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
