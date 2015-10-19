#!/usr/bin/env python3
# Copyright (c) 2015 University of Louisiana at Lafayette.
# All rights reserved.
import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="etatimer",
    version="0.0.2",
    author="Charles LeDoux",
    author_email="charles.a.ledoux@gmail.com",
    description=("Copyright (c) Charles LeDoux"
                 "All rights reserved."),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    license="MIT",
    install_requires=['progressbar2>=3.3.0'],
    py_modules=["etatimer"],
)
