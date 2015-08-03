#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ""


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['jsonrpc_helpers/tests/']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='json-rpc-helpers',
    version='1.0.0',
    packages=find_packages(),

    tests_require=['pytest', 'jsonschema'],
    install_requires=['jsonschema'],
    cmdclass={'test': PyTest},

    author='Lev Orekhov',
    author_email='lev.orekhov@gmail.com',
    url='https://github.com/lorehov/json-rpc-helpers',
    description='Helpers for bootstrapping of JSON-RPC API',
    long_desccription=read('README.md'),
    keywords='json-rpc json-schema validation logging',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='MIT',
)
