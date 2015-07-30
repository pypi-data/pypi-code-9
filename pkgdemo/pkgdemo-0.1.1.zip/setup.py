#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages
version = '0.1.1'
classifiers = [
    "Programming Language :: Python",
    ("Topic :: Software Development :: "
     "Libraries :: Python Modules")]
setup(name='pkgdemo',
      version=version,
      description=("It's my first package,I'm a chinese"),
      classifiers=classifiers,
      keywords='',
      author='Fanglei.Zou(1981)',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
      include_package_data=True,      
      install_requires=['setuptools', 
                        'PasteScript'],
      entry_points="""

      # -*- Entry points: -*-
      [paste.paster_create_template]
      pbp_package = pkgdemo.package:Package
      """)
