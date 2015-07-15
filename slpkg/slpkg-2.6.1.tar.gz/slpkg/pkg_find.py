#!/usr/bin/python
# -*- coding: utf-8 -*-

# pkg_find.py file is part of slpkg.

# Copyright 2014-2015 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Slpkg is a user-friendly package manager for Slackware installations

# https://github.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import sys

from messages import Msg
from sbo.greps import SBoGrep
from pkg.manager import PackageManager
from __metadata__ import MetaData as _meta_


def find_from_repos(pkg):
    """
    Find packages from enabled repositories
    """
    cache = ""
    count_pkg = count_repo = 0
    print("\nPackages with name matching [ {0}{1}{2} ]\n".format(
        _meta_.color["CYAN"], ", ".join(pkg), _meta_.color["ENDC"]))
    Msg().template(78)
    print("| {0}  {1}{2}{3}".format("Repository", "Package", " " * 54, "Size"))
    Msg().template(78)
    try:
        for repo in _meta_.repositories:
            PACKAGES_TXT = PackageManager(pkg).list_lib(repo)
            packages, sizes = PackageManager(pkg).list_greps(repo, PACKAGES_TXT)
            for find, size in zip(packages, sizes):
                for p in pkg:
                    if p in find:
                        if cache != repo:
                            count_repo += 1
                        cache = repo
                        count_pkg += 1
                        ver = sbo_version(repo, find)
                        print("  {0}{1}{2} {3}{4:>11}".format(
                            repo, " " * (12 - len(repo)),
                            find + ver, " " * (53 - len(find + ver)),
                            size))
        print("\nFound summary")
        print("=" * 79)
        print("{0}Total found {1} packages in {2} repositories.{3}\n".format(
            _meta_.color["GREY"], count_pkg, count_repo, _meta_.color["ENDC"]))
    except KeyboardInterrupt:
        print("")   # new line at exit
        sys.exit(0)


def sbo_version(repo, find):
    """
    Add version to SBo packages
    """
    ver = ""
    if repo == "sbo":
        ver = "-" + SBoGrep(find).version()
    return ver
