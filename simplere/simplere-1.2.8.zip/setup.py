#!/usr/bin/env python

from setuptools import setup
from codecs import open


def lines(text):
    """
    Returns each non-blank line in text enclosed in a list.
    See http://pypi.python.org/pypi/textdata for more sophisticated version.
    """
    return [l.strip() for l in text.strip().splitlines() if l.strip()]

setup(
    name='simplere',
    version='1.2.8',
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description='Simpler, cleaner access to regular expressions. Globs too.',
    long_description=open('README.rst', encoding='utf-8').read(),
    url='https://bitbucket.org/jeunice/simplere',
    license='Apache License 2.0',
    packages=['simplere'],
    setup_requires=[],
    install_requires=['mementos'],
    tests_require=['tox', 'pytest', 'pytest-cov', 'coverage', 'six'],
    test_suite="test",
    zip_safe = False,  # actually it is, but this apparently avoids setuptools hacks
    keywords='re regex regexp regular expression glob simple',
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
