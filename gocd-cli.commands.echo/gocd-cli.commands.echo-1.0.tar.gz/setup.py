#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def version():
    from gocd_cli.commands import echo
    return echo.__version__

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='gocd-cli.commands.echo',
    author='Björn Andersson',
    author_email='ba@sanitarium.se',
    license='MIT License',
    description='An example echo command',
    long_description=README,
    version=version(),
    packages=find_packages(exclude=('tests',)),
    cmdclass={'test': PyTest},
    install_requires=[
        'gocd-cli>=0.7,<1.0',
    ],
)
