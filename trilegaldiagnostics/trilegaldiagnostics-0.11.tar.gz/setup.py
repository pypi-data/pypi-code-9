#!/usr/bin/env python

from setuptools import setup

setup(
    name='trilegaldiagnostics',
    author='Phil Rosenfield',
    author_email='philip.rosenfield@unipd.it',
    version='0.11',
    py_modules=['color_by_arg'],
    scripts=['color_by_arg'],
    install_requires=['numpy', 'matplotlib'],
    url='https://github.com/philrosenfield/trilegaldiagnostics'
)