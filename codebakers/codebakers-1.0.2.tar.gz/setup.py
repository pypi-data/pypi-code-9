#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup

try:
    long_description = file('README.rst').read()
except IOError:
    long_description = ''

setup(
    name='codebakers',
    version='1.0.2',
    url='https://github.com/aziontech/codebakers',
    description=u'Zen of Codebakers',
    long_description=long_description,
    author='Mauricio de Abreu Antunes',
    author_email='mauricio.antunes@azion.com',
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=['codebakers'],
    install_requires=['setuptools'],
)
