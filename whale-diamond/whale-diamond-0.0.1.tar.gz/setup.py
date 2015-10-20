#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

AUTHOR = 'Whale Monitoring'
DESCRIPTION = 'Whale Monitoring Diamond Handler'
EMAIL = 'eirik@sylliaas.no'
GIT = 'git@github.com:WhaleMonitoring/whale-diamond.git'
KEYWORDS = 'Monitoring, Linux, Whale'
LICENSE = 'MIT'
VERSION = '0.0.1'

readme = open('README.rst').read()

requirements = [
    'six',
    'whale-api'
]

test_requirements = [
    'pytest',
    'mock',
    'coverage',
]

setup(
    name='whale-diamond',
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
    ],
    tests_require=test_requirements,
)
