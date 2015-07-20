#!/usr/bin/env python2

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

packages = [
    'dynoclick'
]


requires = [
    'click==4.1'
]

setup(
    name='dynoclick',
    version='0.1.2',
    description='',
    long_description=open('README.md').read(),
    author='Alexandr Skurikhin',
    author_email='a@skurih.in',
    url='https://github.com/a-sk/dynoclick',
    scripts=[],
    packages=packages,
    package_data={'': ['LICENSE']},
    install_requires=requires,
    license=open('LICENSE').read(),
)

del os.environ['PYTHONDONTWRITEBYTECODE']
