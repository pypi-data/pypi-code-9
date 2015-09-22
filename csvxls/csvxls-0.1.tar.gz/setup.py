from __future__ import absolute_import

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.pytest_args))


setup(
    name="csvxls",
    description="Functions to read from CSV or XLS(S) files interchangeably",
    author="Yuki Izumi",
    author_email="yuki@kivikakk.ee",
    license="kindest",
    version="0.1",
    packages=["csvxls"],
    install_requires=["six>=1,<2", "xlrd==0.9.3"],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)
