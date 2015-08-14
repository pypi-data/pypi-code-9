#!/usr/bin/env python
from distutils.core import setup

setup(name='ignor',
      version='0.1',
      description='Easily git ignore any file or dir in your git repo',
      url='',
      author='Jay H Patel',
      author_email='jaypatelh@gmail.com',
      packages=['ignor'],
      package_dir={'ignor': '.'},
      scripts=['cmds/ignor'])