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
    name="driver2200087",
    version="0.5",
    author="Chintalagiri Shashank",
    author_email="shashank@chintal.in",
    description="Python Package to interface with Radio Shack's 2200087 Multimeter",
    license="GPLv2",
    keywords="driver multimeter acquisition",
    url="https://github.com/chintal/2200087-Serial-Protocol",
    packages=['driver2200087'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python",
        "Framework :: Twisted",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    install_requires=['crochet>=1.4.0',
                      'pyserial>=2.7',
                      'Twisted>=15.2.1',
                      ],
    platforms='any',
)
