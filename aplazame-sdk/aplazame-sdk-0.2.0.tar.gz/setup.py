import os
import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

    """
    Usage:
    python setup.py test -a "--host=:host --private-token=:token"
    """
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to py.test")
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def get_version(package):
    with open(os.path.join(package, '__init__.py')) as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                         f.read(), re.MULTILINE).group(1)


def get_long_description():
    with open('README.rst', 'r') as f:
        readme = f.read()

    with open('HISTORY.rst', 'r') as f:
        history = f.read()

    return "{0}\n\n{1}".format(readme, history)

setup(
    name='aplazame-sdk',
    version=get_version('aplazame_sdk'),
    description='Python Interface to the Aplazame API',
    long_description=get_long_description(),
    author='calvin',
    author_email='dani@aplazame.com',
    packages=['aplazame_sdk'],
    package_data={'': ['LICENSE']},
    include_package_data=True,
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    zip_safe=False,
    url='https://github.com/aplazame/aplazame-sdk',
    license='Apache 2.0',
    install_requires=['requests>=1.1.0'],
    dependency_links=[
        'https://github.com/kennethreitz/requests'],
    classifiers=[
        'Programming Language :: Python',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    keywords=['python', 'aplazame', 'api', 'rest', 'sdk']
)
