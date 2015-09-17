#!/usr/bin/env python

import sys
from distutils.core import setup
sys.path.insert(0, '.')
import version


setup(name='analyst-remote-control',
      version=version.getVersion(),
      description=open('README.md', 'rb').read(),
      author='Christian Fobel',
      author_email='christian@fobel.net',
      url='https://github.com/wheeler-microfluidics/analyst-remote-control',
      install_requires=['pyzmq'],
      packages=['analyst_remote_control'])
