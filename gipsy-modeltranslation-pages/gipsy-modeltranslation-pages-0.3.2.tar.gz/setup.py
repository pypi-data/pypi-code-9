#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

import os

from pip.req import parse_requirements
from setuptools import setup, find_packages


# allow setup.py to be run from any path and open files
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def get_requirements(filename):
    install_requires = []
    dependency_links = []
    for r in parse_requirements(filename, session=False):
        if hasattr(r, 'link') and r.link and r.link.url:
            r.req.specs = [('<=', '99.99')]
            dependency_links.append(r.link.url+'-99.99')
        install_requires.append(str(r.req))
    return install_requires, dependency_links

install_requires, dependency_links = get_requirements('requirements.txt')
tests_require, dependency_links2 = get_requirements('requirements/test.txt')
dependency_links = list(set(dependency_links + dependency_links2))


setup(
    name='gipsy-modeltranslation-pages',
    version="0.3.2",
    author=u'Rafał Selewońko',
    author_email='rafal@selewonko.com',
    description='Gipsy Modeltranslation Pages',
    url='http://github.org/revsquare/gipsy-modeltranslation-pages',
    packages=find_packages(),
    namespace_packages=['gipsy'],
    include_package_data=True,
    license='MIT',
    long_description=open('README.rst').read(),
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=install_requires,
    dependency_links=dependency_links,
    tests_require=tests_require,
)
