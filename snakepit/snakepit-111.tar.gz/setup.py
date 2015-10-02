#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'snakepit',
          version = '111',
          description = '''Package Python software as an RPM including all dependencies (even the interpreter).''',
          long_description = '''''',
          author = "Valentin Haenel",
          author_email = "valentin@haenel.co",
          license = 'Apache',
          url = 'https://github.com/ImmobilienScout24/snakepit',
          scripts = ['scripts/snakepit'],
          packages = ['snakepit'],
          py_modules = [],
          classifiers = ['Development Status :: 2 - Pre-Alpha', 'Environment :: Console', 'Intended Audience :: Developers', 'Intended Audience :: System Administrators', 'License :: OSI Approved :: Apache Software License', 'Programming Language :: Python', 'Operating System :: POSIX :: Linux', 'Topic :: System :: Software Distribution', 'Topic :: System :: Systems Administration', 'Topic :: System :: Archiving :: Packaging', 'Topic :: Utilities'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
          package_data = {'snakepit': ['TEMPLATE.spec']},   # package data
          install_requires = [ "docopt", "jinja2", "pyyaml", "requests" ],
          
          zip_safe=True
    )
