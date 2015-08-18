#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
from distutils.core import setup


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = ['README.md']
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename) for filename in filenames])
    return {package: filepaths}

setup(
    name='django_hipster_api',
    version='1.6.8',
    packages=get_packages('hipster_api'),
    package_data=get_package_data('hipster_api'),
    long_description=read("hipster_api/README.md"),
    install_requires=['pytz>=2015.4', 'djangorestframework>=3.2.2'],
    url='https://github.com/RustoriaRu/hipster_api',
    license='MIT',
    author='vir-mir',
    keywords='django rest framework',
    author_email='virmir49@gmail.com',
    description='wrapper django rest framework',
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
