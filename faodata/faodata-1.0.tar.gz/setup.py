#!/usr/bin/env python

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)).read()

config = {
    'name': 'faodata',
    'version': '1.0',
    'description': 'Download data from FAO webservice',
    'long_description': read('README.rst'),
    'author': 'Julien Lerat',
    'author_email': 'julien.lerat@gmail.com',
    'license': 'MIT',
    'url': 'https://bitbucket.com/jlerat/faodata',
    'download_url': 'https://bitbucket/jlerat/faodata/downloads',
    'install_requires': [
        'numpy >= 1.7.2',
        'pandas >= 0.16.0',
        'matplotlib >= 1.3.1',
    ],
    'packages': [
        'faodata'
    ],
    'include_package_data': True,
    'package_data': {
        'faodata' : ['*.gz']
        },
    'classifiers': [
        'Operating System :: OS Independent', 
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.6',
        'License :: OSI Approved :: MIT License'
    ],
    'keywords': [
        'FAO',
        'Web Service',
        'GIS'
    ],
    'test_suite': 'tests'
}

setup(**config)

