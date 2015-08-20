#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''setup for shove_leveldb'''

from setuptools import setup, find_packages


def getversion(fname):
    '''Get the __version__ without importing.'''
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return '%s.%s.%s' % eval(line[13:].rstrip())

setup(
    name='shove_leveldb',
    version=getversion('shove_leveldb/__init__.py'),
    description='Object storage frontend using LevelDB',
    long_description=open('README.rst').read(),
    author='L. C. Rees',
    author_email='lcrees@gmail.com',
    url='https://bitbucket.org/lcrees/shove-leveldb',
    license='BSD',
    packages=find_packages(),
    test_suite='shove_leveldb.test',
    install_requires=('shove>=0.6.4', 'leveldb'),
    zip_safe=False,
    keywords='object storage persistence database leveldb',
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
    ],
    entry_points='''
    [shove.stores]
    leveldb=shove_leveldb.store:LevelDBStore
    ''',
)
