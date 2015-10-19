#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("requirements.txt") as f:
    requirements = [req.strip() for req in f.readlines()]

test_requirements = [
    "nose",
    "nose-cov"
]
setup(name='Google-Search-API',
      version='1.1.10',
      url='https://github.com/abenassi/Google-Search-API',
      description='Search in google',
      author='Anthony Casagrande, Agustin Benassi',
      author_email='birdapi@gmail.com, agusbenassi@gmail.com',
      maintainer="Agustin Benassi",
      maintainer_email='agusbenassi@gmail.com',
      license='MIT',
      packages=[
          'google',
          'google.modules',
          'google.tests'
      ],
      package_dir={'google': 'google'},
      include_package_data=True,
      install_requires=requirements,
      keywords="google search images api",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7'
      ],
      setup_requires=['nose>=1.0'],
      test_suite='nose.collector',
      tests_require=test_requirements
      )
