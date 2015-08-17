#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Capsul current version
version_major = 1
version_minor = 0
version_micro = 0

# The following variables are here for backward compatibility in order to
# ease a transition for bv_maker users. They will be removed in a few days.
_version_major = version_major
_version_minor = version_minor
_version_micro = version_micro

# Expected by setup.py: string of form "X.Y.Z"
__version__ = "{0}.{1}.{2}".format(version_major, version_minor, version_micro)

# Expected by setup.py: the status of the project
CLASSIFIERS = ["Development Status :: 5 - Production/Stable",
               "Environment :: Console",
               "Operating System :: Unix",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering",
               "Topic :: Utilities"]

# Project descriptions
description = "PIWS setup"
long_description = """
====================================
Population Imaging Web Service Setup
====================================


Summary
=======

Setup to add all the required CubicWeb cubes when starting a new population
imaging studies.


How to
======

Execute the piws_setup command:

::

    Usage: piws_setup [options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -d DIR, --directory=DIR
                            Specify the directory where the cubes will be cloned.
      -l DEBUG_LEVEL, --level=DEBUG_LEVEL
                            Set the debug level.
"""

# Main setup parameters
NAME = "piws_setup"
ORGANISATION = "CEA"
MAINTAINER = "Antoine Grigis"
MAINTAINER_EMAIL = "antoine.grigis@cea.fr"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/neurospin/piws_setup.git"
DOWNLOAD_URL = ""
LICENSE = "CeCILL-B"
CLASSIFIERS = CLASSIFIERS
AUTHOR = "NSAp developers"
AUTHOR_EMAIL = "antoine.grigis@cea.fr"
PLATFORMS = "OS Independent"
VERSION = __version__
PROVIDES = ["piws_setup"]
REQUIRES = []
EXTRA_REQUIRES = {
    "doc": ["sphinx>=1.0"]
}
