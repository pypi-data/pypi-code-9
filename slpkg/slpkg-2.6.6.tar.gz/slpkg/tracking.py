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
from graph import graph_deps
from blacklist import BlackList
from __metadata__ import MetaData as _meta_

from pkg.find import find_package

from sbo.dependency import Requires
from sbo.search import sbo_search_pkg

from binary.search import search_pkg
from binary.dependency import Dependencies


class TrackingDeps(object):
    """
    View tree of dependencies and also
    highlight packages with color green
    if allready installed and color red
    if not installed.
    """
    def __init__(self, name, repo, flag):
        self.name = name
        self.repo = repo
        self.flag = flag
        self.meta = _meta_
        self.green = self.meta.color["GREEN"]
        self.yellow = self.meta.color["YELLOW"]
        self.cyan = self.meta.color["CYAN"]
        self.red = self.meta.color["RED"]
        self.endc = self.meta.color["ENDC"]
        self.requires = []
        self.dependencies = []
        self.dependencies_list = []
        self.deps_dict = {}

    def run(self):
        """Run tracking dependencies
        """
        Msg().resolving()
        self.repositories()
        if self.find_pkg:
            self.requires = Utils().dimensional_list(self.dependencies_list)
            self.requires.reverse()
            self.dependencies = Utils().remove_dbs(self.requires)
            if self.dependencies == []:
                self.dependencies = ["No dependencies"]
            if self.flag.startswith("--graph="):
                self.deps_tree()
                Msg().done()
                self.graph()
            Msg().done()
            pkg_len = len(self.name) + 24
            print("")    # new line at start
            Msg().template(pkg_len)
            print("| Package {0}{1}{2} dependencies :".format(
                self.cyan, self.name, self.endc))
            Msg().template(pkg_len)
            print("\\")
            print(" +---{0}[ Tree of dependencies ]{1}".format(self.yellow,
                                                               self.endc))
            index = 0
            for pkg in self.dependencies:
                used = self.check_used(pkg)
                self.deps_used(pkg, used)
                if used and self.flag.startswith("--check-deps"):
                    used = "{0} {1}{2}{3}".format(
                        "is dependency -->", self.cyan,
                        ", ".join(used), self.endc)
                else:
                    used = ""
                index += 1
                installed = ""
                if find_package(pkg + self.meta.sp, self.meta.pkg_path):
                    if self.meta.use_colors in ["off", "OFF"]:
                        installed = "* "
                    print(" |")
                    print(" {0}{1}: {2}{3}{4} {5}{6}".format(
                        "+--", index, self.green, pkg,
                        self.endc, installed, used))
                else:
                    print(" |")
                    print(" {0}{1}: {2}{3}{4} {5}".format(
                        "+--", index, self.red, pkg,
                        self.endc, installed))
            if self.meta.use_colors in ["off", "OFF"]:
                print("\n *: Installed\n")
            else:
                print("")    # new line at end
            if self.flag.startswith("--check-deps--graph="):
                self.graph()
        else:
            print("\nNo package was found to match\n")

    def repositories(self):
        """Get dependencies by repositories
        """
        if self.repo == "sbo":
            self.dependencies_list = Requires(self.flag).sbo(self.name)
            self.find_pkg = sbo_search_pkg(self.name)
        else:
            PACKAGES_TXT = Utils().read_file(self.meta.lib_path + "{0}_repo/"
                                             "PACKAGES.TXT".format(self.repo))
            self.names = Utils().package_name(PACKAGES_TXT)
            self.black = BlackList().packages(self.names, self.repo)
            self.dependencies_list = Dependencies(
                self.names, self.repo, self.black).binary(self.name, self.flag)
            self.find_pkg = search_pkg(self.name, self.repo)

    def graph(self):
        """Drawing image dependencies map
        """
        image = self.flag.split("=")[1]
        graph_deps(self.deps_dict, image)

    def check_used(self, pkg):
        """Check if dependencies used
        """
        used = []
        dep_path = self.meta.log_path + "dep/"
        logs = find_package("", dep_path)
        for log in logs:
            deps = Utils().read_file(dep_path + log)
            for dep in deps.splitlines():
                if pkg == dep:
                    used.append(log)
        return used

    def deps_tree(self):
        """Package dependencies image map file
        """
        dependencies = self.dependencies + [self.name]
        if self.repo == "sbo":
            for dep in dependencies:
                deps = Requires(self.flag).sbo(dep)
                if dep not in self.deps_dict.values():
                    self.deps_dict[dep] = Utils().dimensional_list(deps)
        else:
            for dep in dependencies:
                deps = Dependencies(self.names, self.repo,
                                    self.black).binary(dep, self.flag)
                if dep not in self.deps_dict.values():
                    self.deps_dict[dep] = Utils().dimensional_list(deps)

    def deps_used(self, pkg, used):
        """Create dependencies dictionary
        """
        if find_package(pkg + self.meta.sp, self.meta.pkg_path):
            if pkg not in self.deps_dict.values():
                self.deps_dict[pkg] = used
            else:
                self.deps_dict[pkg] += used
