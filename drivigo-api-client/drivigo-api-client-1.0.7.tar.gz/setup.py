#!/usr/bin/env python
# coding: utf-8
import os

from setuptools import setup, find_packages

from drivigo_api_client import version


def path(p):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)


setup(
    name='drivigo-api-client',
    version=version.version,
    description='Client for Drivigo API',
    long_description='Client for Drivigo API',
    author='Georgy Kutsurua',
    author_email='g.kutsurua@gmail.com',
    maintainer='Georgy Kutsurua',
    maintainer_email='g.kutsurua@gmail.com',
    url='https://bitbucket.org/drivigo/api-client',
    packages=find_packages(exclude=['*tests*']),
    keywords="API, Cars, Automobiles, Auto, Specs, Drivigo",
    platforms=['linux'],
    classifiers=(
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ),
    install_requires=(
        'requests>=2.7.0,<2.8.0',
    ),
    license='BSD'
)
