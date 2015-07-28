#!/usr/bin/env python

from distutils.core import setup


setup(name='digital_ocean_api',
      version='0.0.7',
      description='DigitalOcean API wrapper. It is for personal use only, not generic API.',
      author='Tyler Long',
      author_email='tyler4long@gmail.com',
      packages=['digital_ocean_api'],
      install_requires=['requests>=2.7.0'],
      url='https://github.com/tylingsoft',
      license='GPL',
)
