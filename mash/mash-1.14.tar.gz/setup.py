#!/usr/bin/env python

from distutils.core import setup

with open('README.txt') as file:
    long_description = file.read()

setup(name='mash',
      version='1.14',
      description='Python lib for converting dict to objects recursive',
      long_description=long_description,
      author='Roman Lazoryshchak',
      author_email='lazoryshchak@gmail.com',
      url='https://www.python.org/sigs/distutils-sig/',
      py_modules=['Mash']
     )
