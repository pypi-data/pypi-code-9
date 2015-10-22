#!/usr/bin/env python

from setuptools import setup

setup(
    name='colibri2trilegal',
    author='Phil Rosenfield',
    author_email='philip.rosenfield@unipd.it',
    version='2.1',
    url='https://github.com/philrosenfield/colibri2trilegal',
    py_modules=['colibri2trilegal'],
    scripts=['colibri2trilegal'],
    install_requires=['matplotlib', 'numpy']
)
