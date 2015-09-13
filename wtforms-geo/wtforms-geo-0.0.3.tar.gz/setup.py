# -*- coding: utf-8 -*-
"""
WTForms-Geo
~~~~~~~~~~~
"""

from setuptools import setup, find_packages


setup(
    name='wtforms-geo',
    version='0.0.3',
    description='WTForms geojson fields and widgets.',
    long_description=__doc__,
    url='https://github.com/ecarrara/wtforms-geo',
    author='Erle Carrara',
    author_email='carrara.erle@gmail.com',
    license='BSD',
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    keywords='form geo gis',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'WTForms',
        'geojson',
        'shapely',
        'GeoAlchemy2',
    ]
)
