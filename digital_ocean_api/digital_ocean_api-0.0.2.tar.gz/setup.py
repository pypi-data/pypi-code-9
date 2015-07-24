#!/usr/bin/env python

from distutils.core import setup

install_requires = ['requests>=2.7.0']

setup(name='digital_ocean_api',
      version='0.0.2',
      description='DigitalOcean API wrapper. It is for personal use only, not generic API.',
      author='Tyler Long',
      author_email='tyler4long@gmail.com',
      url='https://github.com/tylerlong/digital-ocean-api',
      packages=['digital_ocean_api'],
)
