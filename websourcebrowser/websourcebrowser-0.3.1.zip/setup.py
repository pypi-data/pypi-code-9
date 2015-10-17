#! /usr/bin/env python
# Copyright (C) 2007-2008, Stefan Schwarzer
# see the file LICENSE for the license of this software

"""
setup.py - installation script for Python distutils
"""

import sys

from distutils import core
from distutils import sysconfig


_name = "websourcebrowser"
_package = "websourcebrowser"
_version = "0.3.1"
_data_target = "%s/%s" % (sysconfig.get_python_lib(), _package)

if sys.platform == "win32":
    scripts = ["scripts/wsbrowser.py"]
else:
    scripts = ["scripts/wsbrowser"]

core.setup(
  # installation data
  name=_name,
  version=_version,
  packages=[_package],
  package_dir={_package: ""},
  scripts=scripts,
  data_files=[(_data_target, ["websourcebrowser.css",
                              "README.txt", "README.html"])],
  # metadata
  author="Stefan Schwarzer",
  author_email="sschwarzer@sschwarzer.net",
  url="http://websourcebrowser.sschwarzer.net/",
  description="A program to quickly browse unknown project source files",
  keywords="Source code, browser, web frontend, local, remote",
  license="Open source (MIT license)",
  platforms=["Pure Python (Python version >= 2.3)"],
  long_description="""\
Websourcebrowser makes it easy to visually scan trees of source
code. In particular, you can view the directory tree and the source
code of a file side by side, so you can quickly change to a different
file.""",
  download_url=
    "http://websourcebrowser.sschwarzer.net/trac/attachment/wiki/Download/%s-%s.tar.gz?format=raw" %
    (_name, _version),
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    # any more which apply? (see
    #  http://pypi.python.org/pypi?%3Aaction=list_classifiers )
    "Topic :: Desktop Environment :: File Managers",
    "Topic :: Software Development",
    "Topic :: Utilities",
    ]
  )

