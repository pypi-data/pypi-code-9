#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

AUTHOR = 'Whale Monitoring'
DESCRIPTION = 'Whale Monitoring API'
EMAIL = 'eirik@sylliaas.no'
GIT = 'git@github.com:WhaleMonitoring/whale-api.git'
KEYWORDS = 'Monitoring, Linux, Whale'
LICENSE = 'MIT'
VERSION = '0.0.1'

readme = open('README.rst').read()

requirements = [
    'six',
    'requests==2.8.1'
]

test_requirements = [
    'pytest',
    'mock',
    'coverage',
]

setup(
    name='whale-api',
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme,
    author=AUTHOR,
    author_email=EMAIL,
    url=GIT,
    packages=find_packages(exclude='tests'),
    include_package_data=True,
    install_requires=requirements,
    license=LICENSE,
    zip_safe=False,
    keywords=KEYWORDS,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    tests_require=test_requirements,
)
