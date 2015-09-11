# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

from user_hash.__version__ import VERSION_STRING

setup(
    name='django-user-hash',
    version=VERSION_STRING,
    author=u'Francesc Ortiz',
    author_email='francescortiz@gmail.com',
    packages=find_packages(),
    url='http://gitlab.francescortiz.net/root/pacasite',
    license='GPL',
    description='Hash system for Django',
    long_description='Hash system for Django',
    zip_safe=False,
    include_package_data=True,
    install_requires=[
    ],
)
