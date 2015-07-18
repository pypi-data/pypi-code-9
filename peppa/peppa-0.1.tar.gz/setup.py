#!/usr/bin/env python

import peppa
from setuptools import setup

setup(name='peppa',
    version=peppa.__version__,
    description='A CLI front-end to a running salt-api system',
    author="Seth Miller",
    author_email='seth@sethmiller.me',
    url='https://github.com/iamseth/peppa',
    packages=['peppa'],
    scripts=['bin/peppa'],
    install_requires=[
                      'docopt>=0.6.2',
                      'requests>=2.0',
    ],
)
