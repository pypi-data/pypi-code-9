#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

with open('requirements.txt') as req:
    requirements = req.read().splitlines()

with open('requirements-test.txt') as test_req:
    test_requirements = test_req.read().splitlines()

setup(
    name='precs',
    version='0.1.0a1',
    description="Python implementation of record stream processing utilities.",
    long_description=readme + '\n\n' + history,
    author="Muhammad Umer Azad",
    author_email='umer.azad@gmail.com',
    url='https://github.com/umerazad/precs',
    packages=[
        'precs',
        'precs.processors'
    ],
    py_modules=['precs/precs'],
    entry_points='''
        [console_scripts]
        precs=precs.precs:cli
    ''',
    package_dir={'precs':
                 'precs'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='precs',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
