# -*- coding: utf-8 -*-
import os
from setuptools import setup
from askcli import __author__, __version__, __status__, __name__, __description__, __url__

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "askcli",
    version = __version__,
    author = __author__,
    author_email = "",
    description = (__description__),
    license = "BSD",
    keywords = "scipting menu yes/no question",
    url = __url__,
    package = "askcli",
    packages=['askcli', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
