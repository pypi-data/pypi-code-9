
# Copyright 2015 Chintalagiri Shashank  (Python Wrapper)
# Copyright 2006 DJ Delorie             (Original C code)
# Distributed under the terms of the GPLv2 License.

from __future__ import print_function

import os
from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Build import cythonize
    USE_CYTHON = True
    print("Using Cython")
except ImportError:
    USE_CYTHON = False
    print("Using bundled sym2eps.c")


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if not USE_CYTHON:
    ext = '.c'
else:
    ext = '.pyx'

extensions = [Extension('sym2eps', ["src/_sym2eps.c", "sym2eps" + ext])]

if USE_CYTHON:
    extensions = cythonize(extensions)


setup(
    name="tendril-gedaif-sym2eps",
    version="0.2",
    author="Chintalagiri Shashank",
    author_email="shashank@chintal.in",
    description="gEDA sym2eps Python Wrapper",
    license="GPLv2",
    keywords="utilities",
    url="https://github.com/chintal/tendril-gedaif-sym2eps",
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: C",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    platforms='any',
    ext_modules=extensions,
    requires=[
        'Cython',
        'pytest',
    ]
)
