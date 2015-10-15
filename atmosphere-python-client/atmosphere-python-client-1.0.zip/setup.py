# coding=utf-8

import os

__author__ = 'paoolo'

try:
    from setuptools import setup
except ImportError:
    print 'No setuptools installed, use distutils'
    from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='atmosphere-python-client',
    packages=[
        'atmosphere',
        'atmosphere.appliance',
        'atmosphere.machine',
        'atmosphere.mapping',
        'atmosphere.property'
    ],
    package_dir={
        'atmosphere': 'src/atmosphere',
        'atmosphere.appliance': 'src/atmosphere/appliance',
        'atmosphere.machine': 'src/atmosphere/machine',
        'atmosphere.mapping': 'src/atmosphere/mapping',
        'atmosphere.property': 'src/atmosphere/property'
    },
    install_requires=required,
    version='1.0',
    description='Atmosphere REST API client written in python',
    author=u'Paweł Suder',
    author_email='pawel@suder.info',
    url='https://github.com/dice-cyfronet/atmosphere-python-client',
    download_url='https://github.com/dice-cyfronet/atmosphere-python-client/archive/master.zip',
    keywords=[
        'atmosphere'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    long_description='''\
'''
)
