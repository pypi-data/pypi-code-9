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
    name='namedentities',
    version='1.3.9',
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description='Named (and numeric) HTML entities to/from each other or Unicode',
    long_description=open('README.rst', encoding='utf-8').read(),
    url='http://bitbucket.org/jeunice/namedentities',
    license='Apache License 2.0',
    packages=['namedentities'],
    setup_requires=[],
    install_requires=[],
    tests_require=['tox', 'pytest', 'six>=1.9'],
    test_suite="test",
    zip_safe=False,  # it really is, but this will prevent weirdness
    keywords='HTML entities Unicode named numeric decimal hex hexadecimal glyph character set charset',
    classifiers=lines("""
        Development Status :: 5 - Production/Stable
        Operating System :: OS Independent
        License :: OSI Approved :: Apache Software License
        Intended Audience :: Developers
        Environment :: Web Environment
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
        Topic :: Text Processing :: Filters
        Topic :: Text Processing :: Markup :: HTML
        Topic :: Software Development :: Libraries :: Python Modules
    """)
)
