#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name = 'bottle-msgpack',
    version = '0.0.2',
    description = 'MsgPack integration for Bottle.',
    author = 'Ignacio Juan Martín Benedetti',
    long_description=readme,
    author_email = 'tranceway@gmail.com',
    url = 'https://github.com/nachopro/bottle-msgpack',
    license = 'MIT',
    platforms = 'any',
    py_modules = [
        'bottle_msgpack'
    ],
    install_requires = REQUIREMENTS,
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Bottle'
    ],
)
