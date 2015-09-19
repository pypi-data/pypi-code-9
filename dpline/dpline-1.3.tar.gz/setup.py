#!/usr/bin/python
# -*- coding: utf-8 -*-

# setup.py file is part of dpline.

# Copyright 2015  Dimitris Zlatanidis  <d.zlatanidis@gmail.com>
# All rights reserved.

# dpline is tool to remove duplicate lines from file

# https://github.com/dslackw/dpline

# Alarm is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import os
import sys
import gzip
import shutil
from distutils.core import setup
from dpline.main import (
    __version__,
    __author__,
    __email__
)

setup(
    name="dpline",
    packages=["dpline"],
    scripts=["bin/dpline"],
    version=__version__,
    description="tool to remove duplicate lines from file",
    keywords=["unique", "duplicate", "text", "lines"],
    author=__author__,
    author_email=__email__,
    url="https://github.com/dslackw/dpline",
    package_data={"": ["LICENSE", "README.rst", "ChangeLog.txt"]},
    classifiers=[
        "Classifier: Development Status :: 3 - Alpha",
        "Classifier: Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Classifier: Operating System :: POSIX",
        "Classifier: Operating System :: POSIX :: Linux",
        "Classifier: Operating System :: Unix",
        "Classifier: Programming Language :: Python",
        "Classifier: Programming Language :: Python :: 2",
        "Classifier: Programming Language :: Python :: 3",
        "Classifier: Topic :: Text Processing :: Filters",
        "Classifier: Topic :: Text Processing :: General",
        ],
    long_description=open("README.rst").read()
)

if "install" in sys.argv and sys.platform == "linux2":
    man_path = "/usr/man/man1/"
    if not os.path.exists(man_path):
        os.makedirs(man_path)
    man_page = "man/dpline.1"
    gzip_man = "man/dpline.1.gz"
    print("Installing '{0}' man page".format(gzip_man.split('/')[1]))
    f_in = open(man_page, "rb")
    f_out = gzip.open(gzip_man, 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
    shutil.copy2(gzip_man, man_path)
