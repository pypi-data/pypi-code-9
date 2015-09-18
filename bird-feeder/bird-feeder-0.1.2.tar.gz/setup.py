# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '0.1.2'
description = 'Bird Feeder publishes Thredds metadata catalogs to a Solr index service with birdhouse schema.'
long_description = (
    open('README.rst').read() + '\n' +
    open('AUTHORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

requires = [
    'argcomplete',
    'pysolr',
    'threddsclient',
    #'dateutil',
    'nose',
    ]

classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        ]

setup(name='bird-feeder',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=classifiers,
      keywords='thredds solr python netcdf birdhouse anaconda',
      author='Birdhouse Developers',
      author_email='',
      url='https://github.com/bird-house/bird-feeder',
      license = "Apache License v2.0",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=requires,
      entry_points = {
          'console_scripts': [
              'birdfeeder=birdfeeder:main',
              ]}     
      ,
      )
