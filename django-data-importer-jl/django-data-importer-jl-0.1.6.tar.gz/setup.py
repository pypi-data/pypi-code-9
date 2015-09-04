#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from distutils.core import setup
from setuptools import setup, find_packages
import data_importer

setup(
    name="django-data-importer-jl",
    version=data_importer.get_version(),
    author="Felipe 'chronos' Prenholato",
    author_email="philipe.rp@gmail.com",
    mainteiner="Jaroslaw Lachowski",
    mainteiner_email="jalachowski@gmail.com",
    url="http://github.com/jlachowski/django-data-importer",
    packages = find_packages(exclude=('sampleprojet',)),
    description="Generic, easy to use, file reader and importer with validations like Django forms.",
    long_description="*data_importer* is a importer tool that allow you write "
        "your own importer, with validation for each field and line of imported "
        "file. It come with support for CSV, XLS and XLSX files and a lot of "
        "examples in tests, logging support, and more.",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=[
        "Django >= 1.3.4",
        "openpyxl",
        "xlrd",
        "future"
    ],
    zip_safe = False,
)
