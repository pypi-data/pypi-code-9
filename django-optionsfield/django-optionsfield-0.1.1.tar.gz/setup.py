#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

import os
import sys

from pip.req import parse_requirements
from setuptools import setup
from setuptools.command.test import test as TestCommand

# allow setup.py to be run from any path and open files
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def get_requirements(filename):
    install_requires = []
    dependency_links = []
    for r in parse_requirements(filename, session=False):
        if hasattr(r, 'link') and r.link and r.link.url:
            r.req.specs = [('<=', '99.99')]
            dependency_links.append(r.link.url+'-99.99')
            dependency_links.append(r.link.url)
        install_requires.append(str(r.req))
    return install_requires, dependency_links

install_requires, dependency_links = get_requirements('requirements.txt')

tests_require, dependency_links_tests = get_requirements('requirements.txt')
dependency_links += dependency_links_tests

from optionsfield._version import __version__ as version
description = 'django-optionsfield'


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


setup(
    name='django-optionsfield',
    version=version,
    author=u'Rafał Selewońko',
    author_email='rafal@selewonko.com',
    description=description,
    url='http://github.com/revsquare/django-optionsfield',
    packages=['optionsfield'],
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
    cmdclass={'test': Tox},
)
