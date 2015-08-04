#!/usr/bin/python
# -*- coding: utf-8 -*-

# status_deps.py file is part of slpkg.

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
from graph import Graph
from splitting import split_package
from __metadata__ import MetaData as _meta_

from pkg.find import find_package


class DependenciesStatus(object):
    """Print dependencies status used by packages
    """
    def __init__(self, image):
        self.image = image
        self.meta = _meta_
        self.dmap = {}
        self.count_pkg = 0
        self.count_dep = 0
        self.dep_path = self.meta.log_path + "dep/"
        self.logs = find_package("", self.dep_path)
        if not self.logs:
            self.no_logs()
        self.installed = find_package("", self.meta.pkg_path)

    def data(self):
        """Check all installed packages and create
        dictionary database
        """
        for pkg in self.installed:
            name = split_package(pkg)[0]
            for log in self.logs:
                deps = Utils().read_file(self.dep_path + log)
                for dep in deps.splitlines():
                    if name == dep:
                        if name not in self.dmap.keys():
                            self.dmap[name] = [log]
                            self.count_dep += 1
                        else:
                            self.dmap[name] += [log]
                            self.count_pkg += 1

    def show(self):
        """Show dependencies status
        """
        self.data()
        if self.image:
            Graph(self.image).dependencies(self.dmap)
        grey = self.meta.color["GREY"]
        green = self.meta.color["GREEN"]
        yellow = self.meta.color["YELLOW"]
        endc = self.meta.color["ENDC"]
        print("")
        Msg().template(78)
        print("| {0}{1}{2}".format("Dependencies", " " * 20, "Packages"))
        Msg().template(78)
        for key, value in self.dmap.iteritems():
            print("  {0}{1}{2}{3}{4}{5}{6}".format(
                yellow, key, endc, " " * (32-len(key)),
                green, ", ".join(value), endc))
        print("\nSummary")
        print("=" * 79)
        print("{0}Found {1} dependencies in {2} packages.{3}\n".format(
            grey, self.count_dep, self.count_pkg, endc))

    def no_logs(self):
        """Print message if no logs found
        """
        print("\n  There were no logs files. Obviously it wasn't used the \n"
              "  method of installation with the command: \n"
              "  '$ slpkg -s <repository> <packages>' yet.\n")
        raise SystemExit()
