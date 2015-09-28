#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'cfn-sphere',
          version = '0.1.17',
          description = '''cfn-sphere AWS CloudFormation management cli''',
          long_description = '''cfn-sphere - A CLI tool intended to simplify AWS CloudFormation handling.''',
          author = "Marco Hoyer",
          author_email = "marco_hoyer@gmx.de",
          license = 'APACHE LICENSE, VERSION 2.0',
          url = 'https://github.com/marco-hoyer/cfn-sphere',
          scripts = ['scripts/cf'],
          packages = ['cfn_sphere', 'cfn_sphere.aws', 'cfn_sphere.resolver', 'cfn_sphere.aws.cloudformation'],
          py_modules = [],
          classifiers = ['Development Status :: 4 - Beta', 'Environment :: Console', 'Intended Audience :: Developers', 'Intended Audience :: System Administrators', 'License :: OSI Approved :: Apache Software License', 'Programming Language :: Python', 'Topic :: System :: Systems Administration'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          install_requires = [ "boto", "click", "networkx", "ordereddict", "pyyaml" ],
          
          zip_safe=True
    )
