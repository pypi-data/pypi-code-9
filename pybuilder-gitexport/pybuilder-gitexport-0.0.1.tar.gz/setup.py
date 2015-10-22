#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'pybuilder-gitexport',
          version = '0.0.1',
          description = '''PyBuilder Git Export''',
          long_description = '''Pybuilder plugin to export contents from a git repository''',
          author = "Alex Dowgailenko",
          author_email = "adow@psikon.com",
          license = 'Apache License, Version 2.0',
          url = 'https://github.com/alex-dow/pybuilder_gitexport',
          scripts = [],
          packages = ['pybuilder_gitexport'],
          py_modules = [],
          classifiers = ['Development Status :: 3 - Alpha', 'Environment :: Console', 'Intended Audience :: Developers', 'License :: OSI Approved :: Apache Software License', 'Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 2.7'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          install_requires = [ "dulwich" ],
          
          zip_safe=True
    )
