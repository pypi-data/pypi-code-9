#!/usr/bin/env python

from os.path import exists
from setuptools import setup, find_packages

from easyboto import __version__

setup(
    name='easyboto',
    version=__version__,
    # Your name & email here
    author='Shantanu Oak',
    author_email='shantanu.oak@gmail.com',
    # If you had myseed.tests, you would also include that in this list
    packages=find_packages(),
    # Any executable scripts, typically in 'bin'. E.g 'bin/do-something.py'
    scripts=[],
    # REQUIRED: Your project's URL
    url='https://github.com/shantanuo/easyboto',
    # Put your license here. See LICENSE.txt for more information
    license='',
    # Put a nice one-liner description here
    description='Amazon Cloud made easy',
    long_description=open('README.rst').read() if exists("README.rst") else "",
    # Any requirements here, e.g. "Django >= 1.1.1"
    install_requires=["boto >= 1.0"
        
    ],
)
