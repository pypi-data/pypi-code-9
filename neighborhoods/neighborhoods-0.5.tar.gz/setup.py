#-----------------------------------------------------------------------------#
#   setup.py                                                                  #
#                                                                             #
#   Copyright (c) 2015, StyleSeat, Inc.                                       #
#   All rights reserved.                                                      #
#-----------------------------------------------------------------------------#

from setuptools import find_packages
from setuptools import setup

import neighborhoods

setup(
    name=neighborhoods.__name__,
    version=neighborhoods.__version__,
    description='Lon/lat to Neighborhood for Humans',
    long_description='''
        Neighborhoods converts a longitude and latitude to a neighborhood name
        based on Zillow's data.
    ''',
    url='https://github.com/styleseat/latlong-to-neighborhood',
    author='StyleSeat, Inc.',
    author_email='dev@styleseat.com',
    license=neighborhoods.__license__,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: Apache Software License',
    ],
    keywords='neighborhoods geospatial geo',
    packages=find_packages(exclude=('contrib', 'docs', 'tests*')),
    install_requires=('Fiona', 'Shapely'),
    extras_require={},
    include_package_data=True,
    package_data={'neighborhoods': ['data/*']},
    data_files=tuple(),
    entry_points={},
)
