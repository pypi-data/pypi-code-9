#!/usr/bin/env python
from distutils.core import setup

setup(name='sourcedata',
      description='generate c++ and go source files containing literals',
      version='0.1',
      author='Alex Flint',
      author_email='alex.flint@gmail.com',
      url='https://github.com/alexflint/sourcedata',
      packages=['sourcedata', 'sourcedata.cpp', 'sourcedata.golang'],
      package_dir={'sourcedata': '.'},
      scripts=['cmds/sourcedata']
      )
