#!/usr/bin/python


"""
Setup script for gpsdio-nmea-driver
"""


import os
import sys

from setuptools.command.test import test as TestCommand
from setuptools import find_packages
from setuptools import setup


# https://pytest.org/latest/goodpractises.html
class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['tests']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Import here, because outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open('README.rst') as f:
    readme = f.read().strip()


version = None
author = None
email = None
source = None
with open(os.path.join('gpsdio_nmea_driver', '__init__.py')) as f:
    for line in f:
        if line.strip().startswith('__version__'):
            version = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__author__'):
            author = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__email__'):
            email = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__source__'):
            source = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif None not in (version, author, email, source):
            break


setup(
    author=author,
    author_email=email,
    cmdclass={'test': PyTest},
    description="A gpsdio driver for parsing NMEA sentences directly into GPSd messages.",
    entry_points='''
        [gpsdio.driver_plugins]
        NMEA=gpsdio_nmea_driver.core:NMEA
    ''',
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
        ]
    },
    install_requires=[
        'libais>=0.15',
        'gpsdio>=0.0.7',
        'six'
    ],
    license='Apache 2.0',
    long_description=readme,
    include_package_data=True,
    keywords="gpsdio NMEA driver AIS libais",
    name="gpsdio-nmea-driver",
    packages=find_packages(exclude=['test']),
    url=source,
    version=version,
)
