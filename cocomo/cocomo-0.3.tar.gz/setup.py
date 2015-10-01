#!/usr/bin/env python

import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="cocomo",
    version="0.3",
    author="Chintalagiri Shashank",
    author_email="shashank@chintal.in",
    description="Simple wrapper around SLOCCount",
    license="MIT",
    keywords="utilities",
    url="https://github.com/chintal/cocomo",
    packages=['cocomo'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    platforms='any',
    entry_points={
        'console_scripts': ['cocomo=cocomo.cocomo:main'],
    }
)
