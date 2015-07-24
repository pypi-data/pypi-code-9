#!/usr/bin/env python

from setuptools import setup

def linelist(text):
    """
    Returns each non-blank line in text enclosed in a list.
    """
    return [ l.strip() for l in text.strip().splitlines() if l.split() ]

    # The double-mention of l.strip() is yet another fine example of why
    # Python needs en passant aliasing.


setup(
    name='withref',
    version="0.2.1",
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description="Use Python's with statement to simplify multi-level object dereferences, reminisent of Pascal's with statement",
    long_description=open("README.rst").read(),
    url='https://bitbucket.org/jeunice/withref',
    py_modules=['withref'],
    tests_require=['tox', 'pytest', 'stuf'],
    classifiers=linelist("""
        Development Status :: 4 - Beta
        Operating System :: OS Independent
        License :: OSI Approved :: BSD License
        Intended Audience :: Developers
        Programming Language :: Python
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3.2
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: Implementation :: CPython
        Programming Language :: Python :: Implementation :: PyPy
        Topic :: Software Development :: Libraries :: Python Modules
    """)
)
