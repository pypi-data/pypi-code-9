#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
from distutils.core import setup
from setuptools import find_packages


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django_hipster_api',
    version='1.6.3',
    packages=find_packages(),
    long_description=read("README.md"),
    install_requires='',
    url='https://github.com/RustoriaRu/hipster_api',
    license='MIT',
    author='vir-mir',
    keywords='django rest framework',
    author_email='virmir49@gmail.com',
    description='wrapper django rest framework',
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
