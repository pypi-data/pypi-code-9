# coding: utf8
"""
    geophpy
    -------

    Tools for sub-surface geophysical survey data processing.

    :copyright: Copyright 2014 Lionel Darras and contributors, see AUTHORS.
    :license: GNU GPL v3.

"""
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

README = ''
CHANGES = ''
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except:
    pass

REQUIREMENTS = [
    'netcdf4',    # depends on libhdf5-dev and libnetcdf-dev
    'matplotlib',
    'numpy',
    'pillow',
    'pyshp',
    'simplekml',
    'utm'
]

setup(
    name='GeophPy',
    version='0.20',
#    url='https://github.com/LionelDarras/GeophPy',
    license='GNU GPL v3',
    description='Tools for sub-surface geophysical survey data processing',
    long_description=README + '\n\n' + CHANGES,
    author='Lionel Darras & Philippe Marty',
    author_email='lionel.darras@mom.fr',
    maintainer='Lionel Darras & Philippe Marty',
    maintainer_email='lionel.darras@mom.fr',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS
)
