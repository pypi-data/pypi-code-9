#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import djstatuspage

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = djstatuspage.__version__

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
    name='django-statuspage',
    version=version,
    description="""Your project description goes here""",
    long_description=readme + '\n\n' + history,
    author='Django Statuspage',
    author_email='margus.laak@redfunction.ee',
    url='https://github.com/redfunction/django-statuspage',
    packages=[
        'djstatuspage',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-statuspage',
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
