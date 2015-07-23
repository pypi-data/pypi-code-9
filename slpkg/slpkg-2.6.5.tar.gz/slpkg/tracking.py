#!/usr/bin/python
# -*- coding: utf-8 -*-

# tracking.py file is part of slpkg.

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


from utils import Utils
from messages import Msg
from blacklist import BlackList
from __metadata__ import MetaData as _meta_

from pkg.find import find_package

from sbo.dependency import Requires
from sbo.search import sbo_search_pkg

from binary.search import search_pkg
from binary.dependency import Dependencies


def track_dep(name, repo, flag):
    """
    View tree of dependencies and also
    highlight packages with color green
    if allready installed and color red
    if not installed.
    """
    Msg().resolving()
    if repo == "sbo":
        dependencies_list = Requires(flag="").sbo(name)
        find_pkg = sbo_search_pkg(name)
    else:
        PACKAGES_TXT = Utils().read_file(_meta_.lib_path + "{0}_repo/"
                                         "PACKAGES.TXT".format(repo))
        names = Utils().package_name(PACKAGES_TXT)
        black = BlackList().packages(names, repo)
        dependencies_list = Dependencies(names, repo, black).binary(
            name, flag="")
        find_pkg = search_pkg(name, repo)
    Msg().done()
    if find_pkg:
        requires, dependencies = [], []
        requires = Utils().dimensional_list(dependencies_list)
        requires.reverse()
        dependencies = Utils().remove_dbs(requires)
        if dependencies == []:
            dependencies = ["No dependencies"]
        pkg_len = len(name) + 24
        print("")    # new line at start
        Msg().template(pkg_len)
        print("| Package {0}{1}{2} dependencies :".format(_meta_.color["CYAN"],
                                                          name,
                                                          _meta_.color["ENDC"]))
        Msg().template(pkg_len)
        print("\\")
        print(" +---{0}[ Tree of dependencies ]{1}".format(
            _meta_.color["YELLOW"], _meta_.color["ENDC"]))
        index = 0
        for pkg in dependencies:
            used = check_used(pkg)
            if used and flag == "--check-deps":
                used = "{0} {1}{2}{3}".format(
                    "is dependency -->", _meta_.color["CYAN"],
                    ", ".join(used), _meta_.color["ENDC"])
            else:
                used = ""
            index += 1
            installed = ""
            if find_package(pkg + _meta_.sp, _meta_.pkg_path):
                if _meta_.use_colors in ["off", "OFF"]:
                    installed = "*"
                print(" |")
                print(" {0}{1}: {2}{3}{4} {5}{6}".format(
                    "+--", index, _meta_.color["GREEN"], pkg,
                    _meta_.color["ENDC"], installed, used))
            else:
                print(" |")
                print(" {0}{1}: {2}{3}{4} {5}".format(
                    "+--", index, _meta_.color["RED"], pkg,
                    _meta_.color["ENDC"], installed))
        if _meta_.use_colors in ["off", "OFF"]:
            print("\n *: Installed\n")
        else:
            print("")    # new line at end
    else:
        print("\nNo package was found to match\n")


def check_used(pkg):
    """Check if dependencies used
    """
    used = []
    dep_path = _meta_.log_path + "dep/"
    logs = find_package("", dep_path)
    for log in logs:
        deps = Utils().read_file(dep_path + log)
        for dep in deps.splitlines():
            if pkg == dep:
                used.append(log)
    return used
