#!/usr/bin/env python
# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

import os
import setuptools

version = "0.1.0"


setuptools.setup(
    name="Pynamixel",
    version=version,
    description="Library to use Dynamixel servos supporting several hardwares",
    author="Vincent Jacques",
    author_email="vincent@vincent-jacques.net",
    url="http://pythonhosted.org/Pynamixel",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Communications",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=["pyserial"],
    tests_require=["MockMockMock<0.6.0"],
    test_suite="Pynamixel.tests",
    use_2to3=True,
    command_options={
        "build_sphinx": {
            "version": ("setup.py", version),
            "release": ("setup.py", version),
            "source_dir": ("setup.py", "doc"),
        },
    },
)
