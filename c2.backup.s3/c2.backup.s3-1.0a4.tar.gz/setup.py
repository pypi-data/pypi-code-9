#!/usr/bin/env python

from setuptools import setup, find_packages
import os

version = '1.0a4'

setup(name='c2.backup.s3',
      version=version,
      description='This package supports back up files from local dir to S3 bucket',
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      author='Manabu TERADA',
      author_email='terada@cmscom.jp',
      url='https://bitbucket.org/cmscom/c2.backup.s3',
      packages=find_packages(exclude=['ez_setup']),
      classifiers=[
        "Programming Language :: Python",
        ],
      license='GPL',
      namespace_packages=['c2', 'c2.backup'],
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'boto',
          'PyYAML',
          'FileChunkIO',
        ],
      entry_points = {
        'console_scripts': ['backups3=c2.backup.s3.main:main'],
        }
     )