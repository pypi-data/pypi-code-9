#!/usr/bin/env python
from setuptools import setup,find_packages

setup(
        name='jiemoutils',
        version='0.9',
        description='jiemo utils',
        author='it_account@jiemodai.com',
        author_email='it_account@jiemodai.com',
        url='http://jiemo.co',
        packages=find_packages(),
        install_requires=['django==1.8.2', 'mako==1.0.1', 'pymysql==0.6.6'],
)
