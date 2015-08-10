#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'Cython',
    'numpy',
    'scipy',
    'matplotlib',
    'fipy',
    'ez_setup',
    'ciabatta',
]

test_requirements = [
    'numpy',
    'scipy',
    'fipy',
]

extensions = cythonize([
    Extension("ahoy.numerics", ["ahoy/numerics.pyx"],
              include_dirs=[numpy.get_include()]),
])

setup(
    name='ahoy',
    version='0.1.2',
    description="Agent-based simulations of active particles",
    long_description=readme + '\n\n' + history,
    author="Elliot Marsden",
    author_email='elliot.marsden@gmail.com',
    url='https://github.com/eddiejessup/ahoy',
    packages=setuptools.find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='ahoy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    ext_modules=extensions,
)
