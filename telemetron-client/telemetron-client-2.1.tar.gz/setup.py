#!/usr/bin/env python
import os
from setuptools import setup, find_packages

from telemetron.client import __version__


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

setup(
      name='telemetron-client',
      version=__version__,
      description='Client for Telemetron',
      author='Joao Coutinho',
      author_email='joao.coutinho@mindera.com',
      url='https://bitbucket.org/mindera/telemetry-client-python',
      long_description=README,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      setup_requires=['nose==1.0.0']
      )
