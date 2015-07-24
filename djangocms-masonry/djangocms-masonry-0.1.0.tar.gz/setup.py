#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import djangocms_masonry

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = djangocms_masonry.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()

setup(
    name='djangocms-masonry',
    version=version,
    description="""Djangocms plugin for masonry carousel v1""",
    long_description=readme,
    author='Lee Solway',
    author_email='lee@digitalanvil.co.uk',
    url='https://github.com/digital-anvil/djangocms-masonry',
    packages=[
        'djangocms_masonry',
    ],
    include_package_data=True,
    install_requires=[
        'django-cms >= 3.0',
        'django-appconf >= 1.0.1',
        'jsonfield >= 1.0.3',
    ],
    license="BSD",
    zip_safe=False,
    keywords='djangocms-masonry',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
