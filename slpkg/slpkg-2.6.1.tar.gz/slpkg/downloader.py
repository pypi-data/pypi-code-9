#!/usr/bin/python
# -*- coding: utf-8 -*-

# downloader.py file is part of slpkg.

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


import os
import sys
import subprocess

from messages import Msg
from __metadata__ import MetaData as _meta_


class Download(object):

    def __init__(self, path, url, repo):
        self.path = path
        self.url = url
        self.repo = repo
        self.file_name = ""
        self.meta = _meta_
        self.dir_prefix = ""
        self.downder = self.meta.downder
        self.downder_options = self.meta.downder_options

    def start(self):
        """Download files using wget or other downloader.
        Optional curl and aria2c"""
        dwn_count = 1
        self._directory_prefix()
        for dwn in self.url:
            self.file_name = dwn.split("/")[-1]
            self._check_certificate()
            print("\n[{0}/{1}][ {2}Download{3} ] --> {4}\n".format(
                dwn_count, len(self.url), self.meta.color["GREEN"],
                self.meta.color["ENDC"],
                self.file_name))
            try:
                if self.downder in ["wget", "aria2c"]:
                    subprocess.call("{0} {1} {2}{3} {4}".format(
                                    self.downder, self.downder_options,
                                    self.dir_prefix, self.path, dwn),
                                    shell=True)
                elif self.downder == "curl":
                    subprocess.call("{0} {1} {2}{3} {4}".format(
                                    self.downder, self.downder_options,
                                    self.path, self.file_name, dwn), shell=True)
                self._check_if_downloaded()
                dwn_count += 1
            except KeyboardInterrupt:
                print   # new line at cancel
                sys.exit(0)

    def _directory_prefix(self):
        """Downloader options for specific directory
        """
        if self.downder == "wget":
            self.dir_prefix = "--directory-prefix="
        elif self.downder == "aria2c":
            self.dir_prefix = "--dir="

    def _check_if_downloaded(self):
        """Check if file downloaded
        """
        if not os.path.isfile(self.path + self.file_name):
            print("")
            Msg().template(78)
            print("| Download '{0}' file {1}[ FAILED ]{2}".format(
                self.file_name, self.meta.color["RED"],
                self.meta.color["ENDC"]))
            Msg().template(78)
            print("")
            if not Msg().answer() in ["y", "Y"]:
                sys.exit(0)

    def _check_certificate(self):
        """Check for certificates options for wget
        """
        if (self.file_name.startswith("jdk-") and self.repo == "sbo" and
                self.downder == "wget"):
            certificate = (' --no-check-certificate --header="Cookie: '
                           'oraclelicense=accept-securebackup-cookie"')
            Msg().template(78)
            print("| '{0}' need to go ahead downloading".format(
                certificate[:23]))
            Msg().template(78)
            print("")
            self.downder_options += certificate
            if not Msg().answer() in ["y", "Y"]:
                sys.exit(0)
