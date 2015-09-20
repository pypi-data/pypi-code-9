#  -*- coding: utf-8 -*-
"""
Setuptools script for the Django Condition Chain app.
"""

import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


def required(fname):
    return open(os.path.join(os.path.dirname(__file__),
                             fname)).read().split('\n')


config = {
    "name": "django-condition-chain",
    "version": "0.0.3",
    "namespace_packages": [],
    "packages": find_packages(exclude=["*.tests",
                                       "*.tests.*",
                                       "tests.*",
                                       "tests",
                                       "*.ez_setup",
                                       "*.ez_setup.*",
                                       "ez_setup.*",
                                       "ez_setup",
                                       "*.examples",
                                       "*.examples.*",
                                       "examples.*",
                                       "examples", ]),
    "include_package_data": True,
    "package_data": {"": ["*.js"], },
    "scripts": [],
    "entry_points": {},
    "install_requires": [required('requirements.txt')],
    "tests_require": [required('test-requirements.txt')],
    "test_suite": 'nose.collector',
    "zip_safe": False,
    # Metadata for upload to PyPI
    "author": 'Ellis Percival',
    "author_email": "ellis@0x07.co.uk",
    "description": "Django Condition Chain app",
    "classifiers": ["Programming Language :: Python", ],
    "license": "",
    "keywords": "",
    "url": "",
}

setup(**config)
