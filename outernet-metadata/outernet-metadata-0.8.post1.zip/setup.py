#!/usr/bin/env python

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

SCRIPTDIR = os.path.dirname(__file__) or '.'
PY3 = sys.version_info >= (3, 0, 0)

from outernet_metadata import __version__


def read(fname):
    """ Return content of specified file """
    path = os.path.join(SCRIPTDIR, fname)
    if PY3:
        f = open(path, 'r', encoding='utf8')
    else:
        f = open(path, 'r')
    content = f.read()
    f.close()
    return content


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments for py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='outernet-metadata',
    version=__version__,
    author='Outernet Inc',
    author_email='apps@outernet.is',
    description='Library for working with Outernet metadata',
    license='GPLv3',
    keywords='json, validation, templates, metadata, outernet',
    url='https://github.com/Outernet-Project/bottle-fdsend',
    packages=find_packages(),
    long_description=read('README.rst'),
    install_requires=[
        'chainable-validators>=0.7',
    ],
    extras_require={
        'command line tools':  ['conz>=0.5'],
    },
    entry_points={
        'console_scripts': [
            'metacheck = outernet_metadata.validate:main',
            'metagen = outernet_metadata.template:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 2.7',
    ],
    cmdclass={
        'test': PyTest,
    },
)
