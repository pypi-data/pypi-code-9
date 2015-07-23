#!/usr/bin/env python

from setuptools import setup

setup(
    name='namedentities',
    version='1.6.6',
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description='Named (and numeric) HTML entities to/from each other or Unicode',
    long_description=open('README.rst').read(),
    url='http://bitbucket.org/jeunice/namedentities',
    packages=['namedentities'],
    install_requires=[],
    tests_require=['tox', 'pytest', 'six>=1.9'],
    zip_safe=True,
    keywords='HTML named numeric decimal hex hexadecimal entities Unicode glyph character set charset',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)
