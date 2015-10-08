#!/usr/bin/env python

from distutils.core import setup

# Thanks to Michael Twomey (mick@enginesofcreation.ie) for helping
# with distutils-ification.

setup(name="skim",
    version="1.1",
    long_description="text file viewer with GUI for highlighting and finding multiple words at once",
    author="Drew Perttula and David McClosky",
    author_email="drewp@bigasterisk.com, dmcc@bigasterisk.com",
    url="http://bigasterisk.com/skim",
    download_url="http://projects.bigasterisk.com/skim-1.1.tar.gz",
    package_dir={'skim' : 'src'},
    packages=[
        'skim',
    ],
    scripts=[
        'scripts/skim',
    ],

      classifiers=[ # http://www.python.org/pypi?:action=list_classifiers
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python",
    "Environment :: X11 Applications",
    "Intended Audience :: Developers",
    "Intended Audience :: System Administrators",
    "Intended Audience :: End Users/Desktop",
    "Topic :: Text Processing",
    ],

)
