#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import os
from codecs import open

# with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()


setup(
    name='filter_variants',

    # Versions should comply with PEP440. For a discussion on
    # single-sourcing the version across setup.py and the project code,
    # see http://packaging.python.org/en/latest/tutorial.html#version
    version='0.1',

    description='Filter variants based on frequencies',
    # long_description=long_description,
    # What does your project relate to? Separate with spaces.
    keywords='sequencing exome genome',
    author='Måns Magnusson',
    author_email='mans.magnusson@scilifelab.se',
    license='MIT',

    # The project's main homepage
    url='https://github.com/moonso/filter_variants',

    packages=find_packages(exclude=('tests*', 'docs', 'examples')),

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'Click',
        'setuptools',
        'pytabix'
    ],
    tests_require=[
        'pytest',
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and
    # allow pip to create the appropriate form of executable for the
    # target platform.
    entry_points={
        'console_scripts': [
            'filter_variants = filter_variants.cli.root:cli',
        ],
    },

    # See: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are:
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

        'Environment :: Console',
    ],
)
