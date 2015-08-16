#!/usr/bin/env python
# -*- coding: utf-8 -*-


import setuptools
from numpy.distutils.core import setup
from numpy.distutils.core import Extension as NExtension


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'numpy',
    'scipy',
]

test_requirements = [
    'numpy',
    'scipy',
]

extensions = [
    NExtension('clustrous._periodic_cluster',
               sources=['clustrous/periodic_cluster.f90']),
]

setup(
    name='clustrous',
    version='0.1.1',
    description='Linkage clustering',
    long_description=readme + '\n\n' + history,
    author='Elliot Marsden',
    author_email='elliot.marsden@gmail.com',
    url='https://github.com/eddiejessup/clustrous',
    packages=setuptools.find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    install_requires=requirements,
    license='BSD',
    zip_safe=False,
    keywords='clustrous',
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
