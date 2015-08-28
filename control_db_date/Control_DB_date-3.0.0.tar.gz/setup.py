#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='Control_DB_date',
    version='3.0.0',
    author='ruifengyun',
    author_email='rfyiamcool@163.com',
    packages=find_packages(),
    url='https://github.com/rfyiamcool',
    description='get dbname from date and dbname , According to the monthly',
    long_description=open('README.md').read(),
    install_requires=['IPy==0.81'],
    license='MIT'
)
