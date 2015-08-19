# Martin.Melchior (at) fhnw.ch

import os.path
from setuptools import setup, find_packages

if os.path.exists('README.rst'):
    with open('README.rst') as f:
        long_description = f.read()
else:
    long_description = None
    
setup(
    name = 'euclid_wfm',
    version = '0.4.4',
    description='Euclid pipeline framework',
    long_description=long_description,
    author='Martin Melchior',
    author_email='martin.melchior@fhnw.ch',
    url=None,
    packages = find_packages(),
    install_requires = [ 'enum34', 'Flask' ],
)
