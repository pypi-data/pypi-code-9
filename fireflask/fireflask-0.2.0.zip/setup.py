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
    name='fireflask',
    version='0.2.0',
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description="Simple, beautiful logging from Flask web apps to FireBug console",
    long_description=open('README.rst', encoding='utf-8').read(),
    url='https://bitbucket.org/jeunice/fireflask',
    license='Apache License 2.0',
    py_modules=['fireflask'],
	setup_requires=[],
    install_requires=['firepython>=0.9', 'flask'],
    tests_require=['tox', 'pytest'],
    test_suite="test",
    zip_safe=False,
    keywords='webapp Flask debug log logging FireBug FireLogger FirePython',
    classifiers=lines("""
        Development Status :: 4 - Beta
        Operating System :: OS Independent
        License :: OSI Approved :: Apache Software License
        Intended Audience :: Developers
        Programming Language :: Python
        Programming Language :: Python :: 2.6
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: Implementation :: CPython
        Topic :: Software Development :: Debuggers
        Topic :: Software Development :: Libraries :: Python Modules
        Framework :: Flask
        Environment :: Web Environment
    """)
)
