#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import crispy_admin

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = crispy_admin.__version__

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
    name='django-crispy-admin',
    version=version,
    description="""Django Crispy Admin allows you to edit your forms
    with the handy crispy forms, and bootstrap3 FTW!""",
    long_description=readme + '\n\n' + history,
    author='Enrique Paredes',
    author_email='enrique@iknite.com',
    url='https://github.com/feverup/django-crispy-admin',
    packages=[
        'crispy_admin',
    ],
    include_package_data=True,
    install_requires=[
        'django==1.8',
        'django-crispy-forms>=1.5.2',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-crispy-admin',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
