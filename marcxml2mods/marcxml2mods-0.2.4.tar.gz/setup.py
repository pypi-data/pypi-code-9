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


# Functions ===================================================================
setup(
    name='marcxml2mods',
    version=getVersion(CHANGELOG),
    description="Conversion from MARCXML/OAI to MODS, which is used in NK CZ.",
    long_description=LONG_DESCRIPTION,
    url='https://github.com/edeposit/marcxml2mods',

    author='Edeposit team',
    author_email='edeposit@email.cz',

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",

        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license='MIT',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,

    # scripts=[''],

    zip_safe=False,
    install_requires=[
        "lxml",
        "xmltodict",
        "pydhtmlparser>=2.1.4",
        "marcxml_parser",
        "remove_hairs",
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
