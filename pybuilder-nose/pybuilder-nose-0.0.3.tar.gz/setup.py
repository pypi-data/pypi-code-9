#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'pybuilder-nose',
          version = '0.0.3',
          description = '''PyBuilder Nose Plugin''',
          long_description = '''Pybuilder plugin to work with Nose''',
          author = "Alex Dowgailenko",
          author_email = "adow@psikon.com",
          license = 'Apache License, Version 2.0',
          url = 'https://github.com/alex-dow/pybuilder_nose',
          scripts = [],
          packages = ['pybuilder_nose'],
          py_modules = [],
          classifiers = ['Development Status :: 3 - Alpha', 'Environment :: Console', 'Intended Audience :: Developers', 'License :: OSI Approved :: Apache Software License', 'Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 2.7'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          install_requires = [ "nose", "coverage" ],
          dependency_links = [  ],
          zip_safe=True
    )
