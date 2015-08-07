#!/usr/bin/env python

from setuptools import setup
import sys

_PY26 = sys.version_info[:2] == (2,6)

STUF = 'stuf==0.9.14' if _PY26 else 'stuf>=0.9.16'


def lines(text):
    """
    Returns each non-blank line in text enclosed in a list.
    """
    return [l.strip() for l in text.strip().splitlines() if l.strip()]


setup(
    name='withref',
    version='0.2.5',
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description="Use with to simplify multi-level object dereferences, reminisent of Pascal's with statement",
    long_description=open("README.rst").read(),
    url='https://bitbucket.org/jeunice/withref',
    license='Apache License 2.0',
    py_modules=['withref'],
    setup_requires=[],
    install_requires=[],
    tests_require=['tox', 'pytest', STUF],
    test_suite="test",
    zip_safe=False,  # it really is, but this will prevent weirdness
    keywords='with reference dereference Pascal',
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
