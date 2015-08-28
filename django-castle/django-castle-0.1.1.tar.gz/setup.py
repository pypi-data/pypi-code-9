#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import django_castle

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = django_castle.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-castle',
    version=version,
    description="""A django integration for the castle.io service""",
    long_description=readme + '\n\n' + history,
    author='Jens Alm',
    author_email='jens.alm@prorenata.se',
    url='https://github.com/ulmus/django-castle',
    packages=[
        'django_castle',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-castle',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
