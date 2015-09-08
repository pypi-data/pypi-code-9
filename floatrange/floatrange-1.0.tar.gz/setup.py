#!/bin/env python
# -*- coding: utf-8 -*-
# Author: Laurent Pointal <laurent.pointal@laposte.net>

from distutils.core import setup
import sys
import io

setup(
    name='floatrange',
    version='1.0',
    author='Laurent Pointal',
    author_email='laurent.pointal@laposte.net',
    url='http://perso.limsi.fr/pointal/python:floatrange',
    download_url='https://sourceforge.net/projects/floatrange/',
    description='Support of range() generator with floats.',
    py_modules=['floatrange'],
    keywords=['range', 'float', 'computing', 'generator', 'loop'],
    license='MIT',
    classifiers=[
                'Development Status :: 5 - Production/Stable',
                'Intended Audience :: Science/Research',
                'Natural Language :: English',
                'Operating System :: OS Independent',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.4',
                'License :: OSI Approved :: MIT License',
                'Topic :: Scientific/Engineering',
                'Topic :: Software Development :: Libraries :: Python Modules',
             ],
    long_description=io.open("README.txt", encoding='utf-8').read(),
    )

