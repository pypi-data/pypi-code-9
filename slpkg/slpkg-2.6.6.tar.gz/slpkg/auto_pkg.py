#!/usr/bin/python
# -*- coding: utf-8 -*-

# auto_pkg.py file is part of slpkg.

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
from pkg.manager import PackageManager
from __metadata__ import MetaData as _meta_


class Auto(object):
    """Select Slackware command to install packages"""

    def __init__(self, packages):
        self.packages = packages
        self.meta = _meta_
        self.commands = {
            "i": "installpkg",
            "u": "upgradepkg --install-new",
            "r": "upgradepkg --reinstall"
        }

    def select(self):
        print("\nDetected Slackware binary package for installation:\n")
        for pkg in self.packages:
            print(" " + pkg.split("/")[-1])
        print("")
        Msg().template(78)
        print("| Choose a Slackware command:")
        Msg().template(78)
        for com in sorted(self.commands):
            print("| {0}{1}{2}) {3}{4}{5}".format(
                self.meta.color["RED"], com, self.meta.color["ENDC"],
                self.meta.color["GREEN"], self.commands[com],
                self.meta.color["ENDC"]))
        Msg().template(78)
        try:
            self.choice = raw_input(" > ")
            if self.choice in self.commands.keys():
                sys.stdout.write("   \x1b[1A{0}{1}{2}\n\n".format(
                    self.meta.color["CYAN"], self.commands[self.choice],
                    self.meta.color["ENDC"]))
                sys.stdout.flush()
        except KeyboardInterrupt:
            print("")
            sys.exit(0)
        self.execute()

    def execute(self):
        if self.choice in self.commands.keys():
            if self.choice == "i":
                PackageManager(self.packages).install("")
            elif self.choice in ["u", "r"]:
                PackageManager(self.packages).upgrade(
                    self.commands[self.choice][11:])
