#!/usr/bin/python
# -*- coding: utf-8 -*-

# views.py file is part of slpkg.

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
import pydoc

from slpkg.messages import Msg
from slpkg.blacklist import BlackList
from slpkg.downloader import Download
from slpkg.__metadata__ import MetaData as _meta_

from slpkg.pkg.find import find_package
from slpkg.pkg.build import BuildPackage
from slpkg.pkg.manager import PackageManager

from read import ReadSBo
from remove import delete
from greps import SBoGrep
from compressed import SBoLink
from search import sbo_search_pkg


class SBoNetwork(object):
    """View SBo site in terminal and also read, build or
    install packages
    """
    def __init__(self, name):
        self.name = name
        self.meta = _meta_
        self.choice = ""
        self.FAULT = ""
        self.green = self.meta.color["GREEN"]
        self.red = self.meta.color["RED"]
        self.yellow = self.meta.color["YELLOW"]
        self.cyan = self.meta.color["CYAN"]
        self.grey = self.meta.color["GREY"]
        self.endc = self.meta.color["ENDC"]
        self.build_folder = self.meta.build_path
        Msg().reading()
        grep = SBoGrep(self.name)
        self.data = SBoGrep(name="").names()
        self.blacklist = BlackList().packages(pkgs=self.data, repo="sbo")
        self.sbo_url = sbo_search_pkg(self.name)
        if self.sbo_url:
            self.sbo_desc = grep.description()[len(self.name) + 2:-1]
            self.source_dwn = grep.source().split()
            self.sbo_req = grep.requires()
            self.sbo_dwn = SBoLink(self.sbo_url).tar_gz()
            self.sbo_version = grep.version()
            self.dwn_srcs = self.sbo_dwn.split() + self.source_dwn
        Msg().done()

    def view(self):
        """
        View SlackBuild package, read or install them
        from slackbuilds.org
        """
        if self.sbo_url and self.name not in self.blacklist:
            prgnam = ("{0}-{1}".format(self.name, self.sbo_version))
            self.view_sbo()
            while True:
                self.read_choice()
                if self.choice in ["D", "d"]:
                    Download(path="", url=self.dwn_srcs, repo="sbo").start()
                    break
                elif self.choice in ["R", "r"]:
                    README = ReadSBo(self.sbo_url).readme("README")
                    fill = self.fill_pager(README)
                    pydoc.pager(README + fill)
                elif self.choice in ["F", "f"]:
                    info = ReadSBo(self.sbo_url).info(self.name, ".info")
                    fill = self.fill_pager(info)
                    pydoc.pager(info + fill)
                elif self.choice in ["S", "s"]:
                    SlackBuild = ReadSBo(self.sbo_url).slackbuild(self.name,
                                                                  ".SlackBuild")
                    fill = self.fill_pager(SlackBuild)
                    pydoc.pager(SlackBuild + fill)
                elif self.choice in ["B", "b"]:
                    self.build()
                    delete(self.build_folder)
                    break
                elif self.choice in ["I", "i"]:
                    if not find_package(prgnam + self.meta.sp,
                                        self.meta.pkg_path):
                        self.build()
                        self.install(prgnam)
                        delete(self.build_folder)
                        break
                    else:
                        Msg().template(78)
                        Msg().pkg_found(self.name, self.sbo_version)
                        Msg().template(78)
                        break
                else:
                    break
        else:
            Msg().pkg_not_found("\n", self.name, "Can't view", "\n")

    def view_sbo(self):
        """
        View slackbuild.org
        """
        sbo_url = self.sbo_url.replace("/slackbuilds/", "/repository/")
        br1, br2, fix_sp = "", "", " "
        if self.meta.use_colors in ["off", "OFF"]:
            br1 = "("
            br2 = ")"
            fix_sp = ""
        print("")   # new line at start
        Msg().template(78)
        print("| {0}Package {1}{2}{3} --> {4}".format(self.green,
                                                      self.cyan, self.name,
                                                      self.green,
                                                      self.endc + sbo_url))
        Msg().template(78)
        print("| {0}Description : {1}{2}".format(self.green,
                                                 self.endc, self.sbo_desc))
        print("| {0}SlackBuild : {1}{2}".format(self.green, self.endc,
                                                self.sbo_dwn.split("/")[-1]))
        print("| {0}Sources : {1}{2}".format(
            self.green, self.endc,
            (", ".join([src.split("/")[-1] for src in self.source_dwn]))))
        print("| {0}Requirements : {1}{2}".format(self.yellow,
                                                  self.endc,
                                                  ", ".join(self.sbo_req)))
        Msg().template(78)
        print("| {0}R{1}{2}EADME               View the README file".format(
            self.red, self.endc, br2))
        print("| {0}S{1}{2}lackBuild           View the SlackBuild file".format(
            self.red, self.endc, br2))
        print("| In{0}{1}f{2}{3}o{4}                View the Info file".format(
            br1, self.red, self.endc, br2, fix_sp))
        print("| {0}D{1}{2}ownload             Download this package".format(
            self.red, self.endc, br2))
        print("| {0}B{1}{2}uild                Download and build".format(
            self.red, self.endc, br2))
        print("| {0}I{1}{2}nstall              Download/Build/Install".format(
            self.red, self.endc, br2))
        print("| {0}Q{1}{2}uit                 Quit".format(self.red,
                                                            self.endc, br2))

        Msg().template(78)

    def fill_pager(self, page):
        """
        Fix pager spaces
        """
        tty_size = os.popen("stty size", "r").read().split()
        rows = int(tty_size[0]) - 1
        lines = sum(1 for line in page.splitlines())
        diff = rows - lines
        fill = "\n" * diff
        if diff > 0:
            return fill
        else:
            return ""

    def read_choice(self):
        """
        Return choice
        """
        try:
            self.choice = raw_input("{0}  Choose an option > {1}".format(
                self.grey, self.endc))
        except (KeyboardInterrupt, EOFError):
            print("")
            raise SystemExit()

    def error_uns(self):
        """
        Check if package supported by arch
        before proceed to install
        """
        self.FAULT = ""
        UNST = ["UNSUPPORTED", "UNTESTED"]
        if "".join(self.source_dwn) in UNST:
            self.FAULT = "".join(self.source_dwn)

    def build(self):
        """
        Only build and create Slackware package
        """
        self.error_uns()
        if self.FAULT:
            print("\n{0}The package {1} {2}\n".format(self.red,
                                                      self.FAULT,
                                                      self.endc))
            raise SystemExit()
        sources = []
        if not os.path.exists(self.meta.build_path):
            os.makedirs(self.meta.build_path)
        os.chdir(self.meta.build_path)
        Download(self.meta.build_path, self.dwn_srcs, repo="sbo").start()
        script = self.sbo_dwn.split("/")[-1]
        for src in self.source_dwn:
            sources.append(src.split("/")[-1])
        BuildPackage(script, sources, self.meta.build_path).build()

    def install(self, prgnam):
        """
        Install Slackware package found in /tmp
        directory.
        """
        binary_list = []
        for search in find_package(prgnam, self.meta.output):
            if "_SBo" in search:
                binary_list.append(search)
        try:
            binary = (self.meta.output + max(binary_list)).split()
        except ValueError:
            Msg().build_FAILED(self.sbo_url, prgnam)
            raise SystemExit()
        print("[ {0}Installing{1} ] --> {2}".format(self.green,
                                                    self.endc,
                                                    self.name))
        PackageManager(binary).upgrade(flag="--install-new")
