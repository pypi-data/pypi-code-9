#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'pash>=1.1.0',
    'termcolor>=1.1.0',
    'config-handle>=0.2.1',
    'menugen>=0.1.0'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='cybak',
    version='0.4.2',
    description="A simple backup script for Debian.",
    long_description=readme + '\n\n' + history,
    author="Ian McFarlane",
    author_email='iansmcfarlane@gmail.com',
    url='https://github.com/iansmcf/cybak-lzma',
    scripts=[
        'scripts/cybak'
    ],
    packages=[
        'dirwalker',
    ],
    package_dir={'dirwalker':
                 'dirwalker'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='cybackup',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
