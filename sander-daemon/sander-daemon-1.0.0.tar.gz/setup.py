#!/usr/bin/env python
# -*- coding: utf8 -*-

from setuptools import setup, find_packages, Command

setup(
    name='sander-daemon',
    version='1.0.0',
    summary='Jejik daemon class improved by Server Density',
    author='Sander Marechal',
    maintainer='Diogo Dutra',
    maintainer_email='dutradda@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(exclude=['tests']),
    url='https://github.com/serverdensity/python-daemon'
)
