#!/usr/bin/python
from setuptools import setup, find_packages

setup(
    name='pgpubsub',
    version='0.0.5',
    author='Brent Tubbs',
    author_email='brent.tubbs@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'psycopg2',
    ],
    url='https://bitbucket.org/btubbs/pgpubsub',
    description="A convenient Python interface to Postgres's LISTEN and NOTIFY features.",
    long_description=open('README.rst').read(),
)
