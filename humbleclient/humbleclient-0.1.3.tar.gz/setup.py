#!/usr/bin/env python2

from distutils.core import setup

import humble

name     = "humbleclient"
base_url = "http://chadok.info/humbleclient"
version  = humble.version

with open('README.txt') as file:
    long_description = file.read()

setup(
    name         = name,
    packages     = [],
    version      = version,
    description  = "Non official client for Humble Bundle",
    long_description = long_description,
    author       = "Olivier Schwander",
    author_email = "olivier.schwander@ens-lyon.org",
    url          = base_url,
    download_url = base_url + "/" + name + "-" + version + ".tar.gz",
    py_modules   = ["humble"],
    scripts      = ["humblec"],
    requires     = ["PyYAML", "requests"],
    classifiers  = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        ],
)
