#!/usr/bin/python
# -*- coding: utf-8 -*-

# desc.py file is part of slpkg.

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
from __metadata__ import MetaData as _meta_


class PkgDesc(object):

    def __init__(self, name, repo, paint):
        self.name = name
        self.repo = repo
        self.paint = paint
        self.meta = _meta_
        self.COLOR = ""
        self.lib = ""
        color_text = {
            "red": self.meta.color["RED"],
            "green": self.meta.color["GREEN"],
            "yellow": self.meta.color["YELLOW"],
            "cyan": self.meta.color["CYAN"],
            "grey": self.meta.color["GREY"],
            "": ""
        }
        self.COLOR = color_text[self.paint]
        if self.repo in self.meta.repositories and self.repo != "sbo":
            self.lib = self.meta.lib_path + "{0}_repo/PACKAGES.TXT".format(
                self.repo)
        else:
            self.lib = self.meta.lib_path + "{0}_repo/SLACKBUILDS.TXT".format(
                self.repo)

    def view(self):
        PACKAGES_TXT = Utils().read_file(self.lib)
        print("")   # new line at start
        count = 0
        if self.repo != "sbo":
            for line in PACKAGES_TXT.splitlines():
                if line.startswith(self.name + ":"):
                    print(self.COLOR + line[len(self.name) + 1:] +
                          self.meta.color["ENDC"])
                    count += 1
                    if count == 11:
                        break
        else:
            for line in PACKAGES_TXT.splitlines():
                if (line.startswith(
                        "SLACKBUILD SHORT DESCRIPTION:  " + self.name + " (")):
                    count += 1
                    print(self.COLOR + line[31:] + self.meta.color["ENDC"])
        if count == 0:
            Msg().pkg_not_found("", self.name, "No matching", "\n")
        else:
            print("")   # new line at end
