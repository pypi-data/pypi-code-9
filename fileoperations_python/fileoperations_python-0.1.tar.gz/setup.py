#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='fileoperations_python',
      version='0.1',
      description='Basic I/O stuff for python',
      author='Sertan Senturk',
      author_email='contact@sertansenturk.com',
      url='https://github.com/sertansenturk/fileoperations_python',
      packages=find_packages(exclude=["test"])
)
