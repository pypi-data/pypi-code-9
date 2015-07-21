#!/usr/bin/python
# -*- coding: utf-8 -*-

# config.py file is part of slpkg.

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
import subprocess

from utils import Utils
from __metadata__ import MetaData as _meta_


class Config(object):

    def __init__(self):
        self.config_file = "/etc/slpkg/slpkg.conf"
        self.meta = _meta_

    def view(self):
        """
        View slpkg config file
        """
        print("")   # new line at start
        conf_args = [
            "RELEASE",
            "REPOSITORIES",
            "BUILD_PATH",
            "PACKAGES",
            "PATCHES",
            "CHECKMD5",
            "DEL_ALL",
            "DEL_BUILD",
            "SBO_BUILD_LOG",
            "MAKEFLAGS",
            "DEFAULT_ANSWER",
            "REMOVE_DEPS_ANSWER",
            "SKIP_UNST",
            "RSL_DEPS",
            "DEL_DEPS",
            "USE_COLORS",
            "DOWNDER",
            "DOWNDER_OPTIONS",
            "SLACKPKG_LOG",
            "ONLY_INSTALLED",
            "PRG_BAR"
        ]
        read_conf = Utils().read_file(self.config_file)
        try:
            for line in read_conf.splitlines():
                if not line.startswith("#") and line.split("=")[0] in conf_args:
                    print(line)
                else:
                    print("{0}{1}{2}".format(self.meta.color["CYAN"], line,
                                             self.meta.color["ENDC"]))
        except KeyboardInterrupt:
            print("")
            sys.exit(0)
        print("")   # new line at end

    def edit(self, editor):
        """
        Edit configuration file
        """
        subprocess.call("{0} {1}".format(editor, self.config_file), shell=True)
