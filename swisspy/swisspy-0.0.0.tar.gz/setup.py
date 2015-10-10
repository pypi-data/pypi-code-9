#!/usr/bin/env python3

from distutils.core import setup

setup(name='swisspy',
      version='0.0.0',
      description='Creating a pocket sized toolkit library for any situation.',
      author='Mr Axilus',
      author_email='esmith@projectaxil.us',
      url='https://github.com/mraxilus/swiss.py',
      packages=['swiss'],
      package_dir={'swiss': 'source/swiss'},
)

