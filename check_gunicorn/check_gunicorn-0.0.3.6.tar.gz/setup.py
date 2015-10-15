#! /usr/bin/python
# __author__ = 'sadaqatullah'

import os
from distutils.core import setup

setup(
    # Application name:
    name="check_gunicorn",

    # Version number (initial):
    version="0.0.3.6",

    # Application author details:
    author="Sadaqatullah",
    author_email="sadaqatullah.noonari@gmail.com",

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://pypi.python.org/pypi/check_gunicorn",

    #
    # license="LICENSE.txt",
    description="Check for Gunicorn in Nagios",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "elasticsearch",
        "nagiosplugin",
    ],
    scripts = ["check_gunicorn.py"],
    # script_name= os.getcwd()
)
