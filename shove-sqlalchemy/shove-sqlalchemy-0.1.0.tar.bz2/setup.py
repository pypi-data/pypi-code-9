#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''setup for shove-sqlalchemy'''

from setuptools import setup, find_packages


def getversion(fname):
    '''Get the __version__ without importing.'''
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return '%s.%s.%s' % eval(line[13:].rstrip())

setup(
    name='shove-sqlalchemy',
    version=getversion('shove_sqlalchemy/__init__.py'),
    description='Common object storage frontend using SQLAlchemy',
    long_description=open('README.rst').read(),
    author='L. C. Rees',
    author_email='lcrees@gmail.com',
    url='https://bitbucket.org/lcrees/shove-sqlalchemy',
    license='BSD',
    packages=find_packages(),
    test_suite='shove_sqlalchemy.test',
    install_requires=('shove>=0.6.4', 'sqlalchemy>=0.4'),
    zip_safe=False,
    keywords='object storage persistence database sqlalchemy rdms',
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
    firebird=shove_sqlalchemy.store:DBStore
    mssql=shove_sqlalchemy.store:DBStore
    mysql=shove_sqlalchemy.store:DBStore
    oracle=shove_sqlalchemy.store:DBStore
    postgres=shove_sqlalchemy.store:DBStore
    sqlite=shove_sqlalchemy.store:DBStore
    [shove.caches]
    firebird=shove_sqlalchemy.cache:DBCache
    mssql=shove_sqlalchemy.cache:DBCache
    mysql=shove_sqlalchemy.cache:DBCache
    oracle=shove_sqlalchemy.cache:DBCache
    postgres=shove_sqlalchemy.cache:DBCache
    sqlite=shove_sqlalchemy.cache:DBCache
    ''',
)
