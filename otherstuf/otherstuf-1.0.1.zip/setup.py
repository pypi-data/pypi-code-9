#!/usr/bin/env python

from setuptools import setup
from codecs import open
import sys

_PY26 = sys.version_info[:2] == (2,6)
STUF = 'stuf==0.9.14' if _PY26 else 'stuf>=0.9.16'

def lines(text):
    """
    Returns each non-blank line in text enclosed in a list.
    See http://pypi.python.org/pypi/textdata for more sophisticated version.
    """
    return [l.strip() for l in text.strip().splitlines() if l.strip()]

setup(
    name='otherstuf',
    version='1.0.1',
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description='Attributes-accessible mappings chainstuf (like ChainMap) & counterstuf (like Counter)',
    long_description=open('README.rst', encoding='utf-8').read(),
    url='https://bitbucket.org/jeunice/otherstuf',
    license='Apache License 2.0',
    packages=['otherstuf'],
	setup_requires=[],
    install_requires=[STUF],
    tests_require=['tox', 'pytest'],
    test_suite="test",
    zip_safe=False,
    keywords='Counter ChainMap stuf attribute mapping nested',
    classifiers=lines("""
        Development Status :: 4 - Beta
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
