#!/usr/bin/python
# -*- coding: utf-8 -*-

# autobuild.py file is part of slpkg.

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


from greps import SBoGrep

from slpkg.pkg.build import BuildPackage


class AutoBuild(object):
    """Autobuild package if sources and script is already
    downloaded
    """
    def __init__(self, script, sources, path):
        self.script = script
        self.sources = sources
        self.path = path
        self.sbo_sources = []

    def run(self):
        """Build package and fix ordelist per checksum
        """
        self.info_file()
        for sbo, dwn in zip(self.sbo_sources, self.sources):
            if sbo != dwn:
                # If the list does not have the same order use from .info
                # order.
                BuildPackage(self.script, self.sbo_sources, self.path).build()
                raise SystemExit()
        # If user use the correct order list
        BuildPackage(self.script, self.sources, self.path).build()

    def info_file(self):
        """Grab sources from .info file and store filename
        """
        prgnam = self.script[:-7]
        sources = SBoGrep(prgnam).source().split()
        for source in sources:
            self.sbo_sources.append(source.split("/")[-1])
