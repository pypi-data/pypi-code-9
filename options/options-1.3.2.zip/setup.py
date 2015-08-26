#!/usr/bin/env python

from setuptools import setup
from codecs import open
import sys

_PY3 = sys.version_info[0] == 3
_PY26 = sys.version_info[:2] == (2,6)


def lines(text):
    """
    Returns each non-blank line in text enclosed in a list.
    See http://pypi.python.org/pypi/textdata for more sophisticated version.
    """
    return [l.strip() for l in text.strip().splitlines() if l.strip()]


STUF = 'stuf==0.9.14' if _PY26 else 'stuf>=0.9.16'

setup(
    name='options',
    version='1.3.2',
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description='Simple, super-flexible options. Does magic upon request.',
    long_description=open('README.rst', encoding='utf-8').read(),
    url='https://bitbucket.org/jeunice/options',
    license='Apache License 2.0',
    packages=['options'],
    setup_requires=[],
    install_requires=[STUF, 'six>=1.9.0', 'nulltype>=2.1.1'],
    tests_require = ['tox', 'pytest', 'pytest-cov', 'coverage', 'six'],
    test_suite="test",
    zip_safe=False,
    keywords='options config configuration parameters arguments',
    classifiers=lines("""
        Development Status :: 5 - Production/Stable
        Operating System :: OS Independent
        License :: OSI Approved :: Apache Software License
        Intended Audience :: Developers
        Programming Language :: Python
        Programming Language :: Python :: 2
        Programming Language :: Python :: 2.6
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.2
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: Implementation :: CPython
        Programming Language :: Python :: Implementation :: PyPy
        Topic :: Software Development :: Libraries :: Python Modules
    """)
)
