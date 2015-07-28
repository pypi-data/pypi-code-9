import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'kvpbase'))

import version

setup(
  name='kvpbase',
  version=version.VERSION,
  license='MIT',
  description='kvpbase Python SDK',
  author=['Joel Christner'],
  author_email='joel@maraudersoftware.com',
  url='http://www.kvpbase.com/',
  packages=['kvpbase']
)
