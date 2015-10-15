# -*- python -*-
# -*- coding: utf-8 -*-

from setuptools import setup, Extension

version = '0.1'


setup(name='python-recode',
      version=version,
      description='A Python extension to recode text files',
      author='Frederic Gobry',
      author_email='gobry@pybliographer.org',
      maintainer="Germán Poo-Caamaño",
      maintainer_email='gpoo@gnome.org',
      url='https://github.com/pybliographer/python-recode',
      license='GPL',
      long_description='''
This module contains a simple binding to GNU Recode.

It requires the GNU Recode and its development header.

''',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
          'Topic :: Text Processing :: Filters',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
      ],
      keywords='recode text-processing',
      ext_modules=[
          Extension('recode', ['recodemodule.c'],
                    libraries=['recode'])
      ])
