import sys

import os
from setuptools import setup
from setuptools.command.test import test
from pytest_envfiles import __version__


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class PyTest(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='pytest-envfiles',
    description="A py.test plugin that parses environment files before running tests",
    long_description=read('README.rst'),
    version=__version__,
    author='Jonathan Enzinna',
    author_email='jonnyfunfun@gmail.com',
    url='https://github.com/JonnyFunFun/pytest-envfiles',
    packages=['pytest_envfiles'],
    entry_points={'pytest11': ['env = pytest_envfiles.plugin']},
    install_requires=['pytest>=2.6.0'],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ]
)