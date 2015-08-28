#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pylfu',
    version='2.0.1',
    author='ruifengyun',
    author_email='rfyiamcool@163.com',
    packages=find_packages(),
    url='https://github.com/rfyiamcool',
    description='python Lfu cache service ',
    long_description=open('README.rst').read(),
    license='MIT'
)
