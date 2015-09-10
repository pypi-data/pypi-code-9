#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'snakepit',
          version = '86',
          description = '''Package Python software as an RPM including all dependencies (even the interpreter).''',
          long_description = '''''',
          author = "Valentin Haenel",
          author_email = "valentin@haenel.co",
          license = 'Apache',
          url = 'https://github.com/ImmobilienScout24/snakepit',
          scripts = ['scripts/snakepit'],
          packages = ['snakepit'],
          py_modules = [],
          classifiers = ['Development Status :: 3 - Alpha', 'Programming Language :: Python'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
          package_data = {'snakepit': ['TEMPLATE.spec']},   # package data
          install_requires = [ "docopt", "jinja2", "pyyaml" ],
          
          zip_safe=True
    )
