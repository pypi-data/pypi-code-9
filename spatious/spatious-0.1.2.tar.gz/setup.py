#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
from setuptools import setup
from distutils.extension import Extension
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
    'cellulist',
]

test_requirements = [
    'Cython',
    'numpy',
    'scipy',
    'cellulist',
]

extensions = cythonize([
    Extension('spatious.distance_numerics',
              ['spatious/distance_numerics.pyx'],
              include_dirs=[numpy.get_include()]),
    Extension('spatious.geom_numerics',
              ['spatious/geom_numerics.pyx'],
              include_dirs=[numpy.get_include()]),
])

setup(
    name='spatious',
    version='0.1.2',
    description='Distance and geometry utilities',
    long_description=readme + '\n\n' + history,
    author='Elliot Marsden',
    author_email='elliot.marsden@gmail.com',
    url='https://github.com/eddiejessup/spatious',
    packages=setuptools.find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    install_requires=requirements,
    license='BSD',
    zip_safe=False,
    keywords='spatious',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
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
