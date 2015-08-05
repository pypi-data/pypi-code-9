#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import threebot_stats

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = threebot_stats.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')
classifiers = [c for c in open('classifiers').read().splitlines() if '#' not in c]

setup(
    name='threebot-stats',
    version=version,
    description="""Your project description goes here""",
    long_description=readme + '\n\n' + history,
    author='arteria GmbH',
    author_email='admin@arteria.ch',
    url='https://github.com/arteria/3bot-stats',
    packages=[
        'threebot_stats',
    ],
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    license="BSD",
    zip_safe=False,
    keywords='3bot-stats',
    classifiers=classifiers,
)
