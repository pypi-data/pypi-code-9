#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from setuptools import setup

setup(
    name='pyscrambler',
    version='0.0.11',
    description='Concept data scrambler using permutations as a basis',
    url='https://github.com/saxbophone/pyscrambler',
    author='Joshua Saxby',
    author_email='joshua.a.saxby@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Security :: Cryptography'
    ],
    packages=['pyscrambler', 'pyscrambler.scramblers'],
    install_requires=['bitstring==3.1.3',
                      'oset==0.1.3'],
    extras_require={
        'test': ['coverage==3.7.1'],
    },
    zip_safe=False
)
