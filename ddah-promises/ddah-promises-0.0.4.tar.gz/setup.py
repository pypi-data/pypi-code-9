#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

file_dir = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    filepath = os.path.join(file_dir, filename)
    return open(filepath).read()


# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ddah-promises',
    version='0.0.4',
    packages=['promises'],
    include_package_data=True,
    license='Affero',
    description='Promises app.',
    long_description=read_file('README.rst'),
    test_suite='runtests.runtests',
    url='http://github.com/ciudadanointeligente/ddah-promises',
    author=u'Felipe Álvarez / Juan Pablo Pérez Trabucco',
    author_email='lab@ciudadanointeligente.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ],
    install_requires=[
        'django-popolo',
        'django-taggit',
    ],
    dependency_links=[
        'http://github.com/openpolis/django-popolo/tarball/master#egg=django-popolo'
    ],
)
