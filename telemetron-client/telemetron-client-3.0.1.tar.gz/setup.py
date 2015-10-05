#!/usr/bin/env python
import os
from setuptools import setup, find_packages

from telemetronclient import __version__


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()


requires = ["urllib3", "certifi"]

version = __version__

"""
Optionally include git revision
"""
# git_label = None
# try:
#     import subprocess
#     git_label = subprocess.check_output(["git", "describe"])
# except OSError:
#     pass
#
# if git_label:
#     version = "%s (%s)" % (__version__, git_label.strip())


setup(
      name='telemetron-client',
      version=version,
      description='Client for Telemetron',
      author='Joao Coutinho',
      author_email='joao.coutinho@mindera.com',
      url='https://bitbucket.org/mindera/telemetry-client-python',
      long_description=README,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires
  )
