#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Setup script for hdsubnetfinder

To install, run:

python setup.py install

"""

from setuptools import setup, find_packages

setup(
    name='hdsubnetfinder',
    version='0.1.0',
    description='Heat Diffusion Sub-network Finder',
    long_description='Sub-network finder using heat diffusion simulation.',
    author='Daniel Carlin',
    author_email='kono@ucsd.edu',
    url='https://github.com/idekerlab/hdsubnetfinder',
    license='MIT License',
    install_requires=[
        'requests',
        'ndex',
        'python-igraph',
        'pyparsing',
        'numpy',
        'scipy'
    ],
    keywords=['bioinformatics', 'graph', 'network', 'cytoscape'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    test_suite='tests',
    packages=find_packages(),
    include_package_data=True,
)
