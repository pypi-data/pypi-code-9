#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from setuptools import setup, find_packages

from docs import getVersion


# Variables ===================================================================
CHANGELOG = open('CHANGES.rst').read()
LONG_DESCRIPTION = "\n\n".join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    CHANGELOG
])


# Actual setup definition =====================================================
setup(
    name='edeposit.amqp.harvester',
    version=getVersion(CHANGELOG),
    description="Metadata harvester of the books printed by specific publishers.",
    long_description=LONG_DESCRIPTION,
    url='https://github.com/edeposit/edeposit.amqp.harvester/',

    author='Edeposit team',
    author_email='edeposit@email.cz',

    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license='MIT',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    scripts=[
        'bin/edeposit_harvester_test.py'
    ],

    namespace_packages=['edeposit', 'edeposit.amqp'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'pyyaml',
        'httpkie',
        'pydhtmlparser>=2.0.5',
        'edeposit.amqp.aleph',
    ],
    extras_require={
        "test": [
            "pytest"
        ],
        "docs": [
            "sphinx",
            "sphinxcontrib-napoleon",
        ]
    },
)
