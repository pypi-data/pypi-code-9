#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='qualpay',
    version='1.0.1',
    author='Derek Payton',
    author_email='derek.payton@gmail.com',
    description='Python bindings for Qualpay',
    keywords='payment processing qualpay',
    license='MIT',
    url='https://github.com/dmpayton/qualpay-python',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(include=('qualpay',)),
    install_requires=['requests'],
)
