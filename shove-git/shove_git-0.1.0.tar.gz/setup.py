#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''setup for shove using git'''

from setuptools import setup, find_packages


def getversion(fname):
    '''Get the __version__ without importing.'''
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return '%s.%s.%s' % eval(line[13:].rstrip())

setup(
    name='shove_git',
    version=getversion('shove_git/__init__.py'),
    description='Object storage frontend using Git',
    long_description=open('README.rst').read(),
    author='L. C. Rees',
    author_email='lcrees@gmail.com',
    url='https://bitbucket.org/lcrees/shove_git',
    license='BSD',
    packages=find_packages(),
    test_suite='shove_git.test',
    install_requires=('shove>=0.6.4', 'dulwich'),
    zip_safe=False,
    keywords='object storage persistence database git',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database :: Front-Ends',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',        
        'Framework :: Setuptools Plugin',        
    ],
    entry_points='''
    [shove.stores]
    git=shove_git.store:GitStore
    ''',
)
