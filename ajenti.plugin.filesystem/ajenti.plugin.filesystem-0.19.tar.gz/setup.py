#!/usr/bin/env python
from setuptools import setup, find_packages

import os

__requires = filter(None, open('requirements.txt').read().splitlines())

setup(
    name='ajenti.plugin.filesystem',
    version='0.19',
    install_requires=__requires,
    description='Filesystem API',
    long_description='A Filesystem API plugin for Ajenti panel',
    author='Ajenti project',
    author_email='e@ajenti.org',
    url='http://ajenti.org',
    packages=find_packages(),
    include_package_data=True,
)