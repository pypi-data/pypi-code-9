#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'rfalke_fibo_pyb',
          version = '1.0.dev0',
          description = '''''',
          long_description = '''''',
          author = "",
          author_email = "",
          license = '',
          url = '',
          scripts = [],
          packages = ['codecentric'],
          py_modules = [],
          classifiers = ['Development Status :: 3 - Alpha', 'Programming Language :: Python'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          install_requires = [ "sh>=1.11" ],
          
          zip_safe=True
    )
