# -*- coding: utf-8 -*-
import os
from setuptools import setup
from askcli import __author__, __version__, __status__, __name__, __description__, __url__

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
    classifiers=[
    	"Development Status :: 5 - Production/Stable",
    	"Environment :: Console",
        "License :: OSI Approved :: BSD License",
    ],
)
