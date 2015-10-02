#!/usr/bin/env python

from setuptools import setup, find_packages

#one line description
with open('DESCRIPTION') as F:
    description = F.read().strip()

#version number
with open('VERSION') as F:
    version = F.read().strip()

entry_points = {
    'console_scripts': [
        'mus = mus.cli:dispatch'
        ]}

setup(name='mus',
      version=version,
      description=description,
      author='Mark Fiers',
      author_email='mark.fiers.42@gmail.com',
      entry_points = entry_points,
      include_package_data=True,
      url='https://encrypted.google.com/#q=mus&safe=off',
      packages=find_packages(),
      install_requires=[
          'Leip',
          'pytz',
          'python-dateutil',
          'colored',
          'pymongo',
          'path.py',
      ],
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        ]
     )
