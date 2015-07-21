#!/usr/bin/python
####################################################################
# FILENAME: setup.py
# PROJECT: twisted_cql
# DESCRIPTION: Install Twisted CQL client 
#              (thin wrapper around Datastax cassandra-driver client.)
# 
#               Requires: Twisted >= 15.0.0
#                         cassandra-driver >= 2.5.1
#                         blist >= 1.3.6
#
####################################################################
# (C)2015 DigiTar Inc., All Rights Reserved
# Licensed under BSD license. See LICENSE file.
####################################################################

from setuptools import setup, find_packages
 
version = '0.5.8'
 
setup(name='twisted_cql',
      version=version,
      description="Twisted CQL client.",
      long_description="""Thin wrapper around Datastax cassandra-driver client.""",
      classifiers=[],
      keywords='twisted cql cassandra datastax',
      author='DigiTar',
      author_email='support@digitar.com',
      url='https://github.com/williamsjj/twisted_cql',
      license='BSD Simplified',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'old*']),
      zip_safe=False,
      install_requires=["Twisted>=15.0",
                        "cassandra-driver>=2.5.1",
                        "blist>=1.3.6"]
    )
