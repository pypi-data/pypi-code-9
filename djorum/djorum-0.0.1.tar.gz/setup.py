#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import djorum

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = djorum.__version__

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
    name='djorum',
    version=version,
    description="""Simple Django Forum""",
    long_description=readme + '\n\n' + history,
    author='Andrew Blaney',
    author_email='andrewblaney6@gmail.com',
    url='https://github.com/andrewblaney/djorum',
    packages=[
        'djorum',
    ],
    include_package_data=True,
    install_requires=[
        'django-mptt==0.7.4',
        'django-autoslug==1.8.0'
    ],
    license="BSD",
    zip_safe=False,
    keywords='djorum',
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
