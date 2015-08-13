#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name = "pystk500v2",
    version = "0.2.0",
    packages = find_packages(),
    author = "David Ko",
    author_email = "david@barobo.com",
    description = "Python functions to parse and program AVR devices with the STK500V2 protocol.",
    license = "GPL",
    )


