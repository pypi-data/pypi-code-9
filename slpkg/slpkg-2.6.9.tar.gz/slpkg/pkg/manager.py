#!/usr/bin/python
# -*- coding: utf-8 -*-

# manager.py file is part of slpkg.

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

from slpkg.utils import Utils
from slpkg.messages import Msg
from slpkg.splitting import split_package
from slpkg.installed import GetFromInstalled
from slpkg.__metadata__ import MetaData as _meta_

from slpkg.pkg.find import find_package


class PackageManager(object):
    """Package manager class for install, upgrade,
    reinstall, remove, find and display packages"""
    def __init__(self, binary):
        self.binary = binary
        self.meta = _meta_
        self.skip = ""

    def install(self, flag):
        """Install Slackware binary packages
        """
        for pkg in self.binary:
            try:
                subprocess.call("installpkg {0} {1}".format(flag, pkg),
                                shell=True)
                check = pkg[:-4].split("/")[-1]
                if os.path.isfile(self.meta.pkg_path + check):
                    print("Completed!\n")
            except (subprocess.CalledProcessError, KeyboardInterrupt):
                self._not_found("Can't install", self.binary, pkg)

    def upgrade(self, flag):
        """Upgrade Slackware binary packages with new
        """
        for pkg in self.binary:
            try:
                subprocess.call("upgradepkg {0} {1}".format(flag, pkg),
                                shell=True)
                check = pkg[:-4].split("/")[-1]
                if os.path.isfile(self.meta.pkg_path + check):
                    print("Completed!\n")
            except (subprocess.CalledProcessError, KeyboardInterrupt):
                self._not_found("Can't upgrade", self.binary, pkg)

    def _not_found(self, message, binary, pkg):
        if len(binary) > 1:
            bol = eol = ""
        else:
            bol = eol = "\n"
        Msg().pkg_not_found(bol, pkg, message, eol)

    def remove(self, flag, extra):
        """Remove Slackware binary packages
        """
        self.flag = flag
        self.extra = extra
        self.dep_path = self.meta.log_path + "dep/"
        dependencies, rmv_list = [], []
        self.removed = self._view_removed()
        if not self.removed:
            print("")   # new line at end
        else:
            msg = "package"
            if len(self.removed) > 1:
                msg = msg + "s"
            try:
                if self.meta.default_answer in ["y", "Y"]:
                    remove_pkg = self.meta.default_answer
                else:
                    remove_pkg = raw_input(
                        "\nAre you sure to remove {0} {1} [y/N]? ".format(
                            str(len(self.removed)), msg))
            except KeyboardInterrupt:
                print("")   # new line at exit
                sys.exit(0)
            if remove_pkg in ["y", "Y"]:
                self._check_if_used(self.binary)
                for rmv in self.removed:
                    # If package build and install with "slpkg -s sbo <package>"
                    # then look log file for dependencies in /var/log/slpkg/dep,
                    # read and remove all else remove only the package.
                    if (os.path.isfile(self.dep_path + rmv) and
                            self.meta.del_deps in ["on", "ON"]):
                        dependencies = self._view_deps(self.dep_path, rmv)
                        if self._rmv_deps_answer() in ["y", "Y"]:
                            rmv_list += self._rmv_deps(dependencies, rmv)
                        else:
                            rmv_list += self._rmv_pkg(rmv)
                    else:
                        rmv_list += self._rmv_pkg(rmv)
                # Prints all removed packages
                self._reference_rmvs(rmv_list)

    def _rmv_deps_answer(self):
        """Remove dependencies answer
        """
        if self.meta.remove_deps_answer in ["y", "Y"]:
            remove_dep = self.meta.remove_deps_answer
        else:
            try:
                remove_dep = raw_input(
                    "\nRemove dependencies (maybe used by "
                    "other packages) [y/N]? ")
                print("")
            except KeyboardInterrupt:
                print("")  # new line at exit
                sys.exit(0)
        return remove_dep

    def _view_removed(self):
        """View packages before removed
        """
        removed = []
        print("\nPackages with name matching [ {0}{1}{2} ]\n".format(
            self.meta.color["CYAN"], ", ".join(self.binary),
            self.meta.color["ENDC"]))
        for pkg in self.binary:
            pkgs = find_package(pkg + self.meta.sp, self.meta.pkg_path)
            if pkgs:
                print("[ {0}delete{1} ] --> {2}".format(
                    self.meta.color["RED"], self.meta.color["ENDC"], pkgs[0]))
                removed.append(pkg)
            else:
                Msg().pkg_not_found("", pkg, "Can't remove", "")
        return removed

    def _view_deps(self, path, package):
        """View dependencies for before remove
        """
        dependencies = Utils().read_file(path + package)
        print("")   # new line at start
        Msg().template(78)
        print("| Found dependencies for package {0}:".format(package))
        Msg().template(78)
        for dep in dependencies.splitlines():
            if GetFromInstalled(dep).name():
                print("| {0}{1}{2}".format(self.meta.color["RED"], dep,
                                           self.meta.color["ENDC"]))
        Msg().template(78)
        return dependencies

    def _removepkg(self, package):
        """removepkg Slackware command
        """
        try:
            subprocess.call("removepkg {0} {1}".format(self.flag, package),
                            shell=True)
            if os.path.isfile(self.dep_path + package):
                os.remove(self.dep_path + package)  # remove log
        except KeyboardInterrupt:
            print("")
            sys.exit(0)

    def _rmv_deps(self, dependencies, package):
        """Remove dependencies
        """
        removes = []
        deps = dependencies.split()
        deps.append(package)
        self._check_if_used(deps)
        for dep in deps:
            if (dep not in self.skip and
                    find_package(dep + self.meta.sp, self.meta.pkg_path)):
                self._removepkg(dep)
                removes.append(dep)
        return removes

    def _rmv_pkg(self, package):
        """Remove one signle package
        """
        if (find_package(package + self.meta.sp, self.meta.pkg_path) and
                package not in self.skip):
            self._removepkg(package)
        return package.split()

    def _skip_remove(self):
        """Skip packages from remove
        """
        Msg().template(78)
        print("| Insert packages to exception removal:")
        Msg().template(78)
        try:
            self.skip = raw_input(" > ").split()
        except KeyboardInterrupt:
            print("")
            sys.exit(0)
        for s in self.skip:
            if s in self.removed:
                self.removed.remove(s)

    def _check_if_used(self, removes):
        """Check package if dependencies for another package
        before removed"""
        if self.extra == "--check-deps":
            print("")
            view = False
            package, dependency = [], []
            for pkg in find_package("", self.dep_path):
                deps = Utils().read_file(self.dep_path + pkg)
                for rmv in removes:
                    if GetFromInstalled(rmv).name() and rmv in deps.split():
                        view = True
                        package.append(pkg)
                        dependency.append(rmv)
            if view:
                Msg().template(78)
                print("| {0}{1}{2}".format(
                    self.meta.color["RED"], " " * 30 + "!!! WARNING !!!",
                    self.meta.color["ENDC"]))
                Msg().template(78)
                for p, d in zip(package, dependency):
                    print("| {0}{1}{2} is dependency of the package --> "
                          "{3}{4}{5}".format(self.meta.color["YELLOW"], d,
                                             self.meta.color["ENDC"],
                                             self.meta.color["GREEN"], p,
                                             self.meta.color["ENDC"]))
                Msg().template(78)
                self._skip_remove()

    def _reference_rmvs(self, removes):
        """Prints all removed packages
        """
        print("")
        Msg().template(78)
        print("| Total {0} packages removed".format(len(removes)))
        Msg().template(78)
        for pkg in removes:
            if not find_package(pkg + self.meta.sp, self.meta.pkg_path):
                print("| Package {0} removed".format(pkg))
            else:
                print("| Package {0} not found".format(pkg))
        Msg().template(78)
        print("")   # new line at end

    def find(self):
        """Find installed Slackware packages
        """
        matching = size = 0
        print("\nPackages with matching name [ {0}{1}{2} ]\n".format(
            self.meta.color["CYAN"], ", ".join(self.binary),
            self.meta.color["ENDC"]))
        for pkg in self.binary:
            for match in find_package("", self.meta.pkg_path):
                if pkg in match:
                    matching += 1
                    print("[ {0}installed{1} ] - {2}".format(
                        self.meta.color["GREEN"], self.meta.color["ENDC"],
                        match))
                    data = Utils().read_file(self.meta.pkg_path + match)
                    for line in data.splitlines():
                        if line.startswith("UNCOMPRESSED PACKAGE SIZE:"):
                            if "M" in line[26:]:
                                size += float(line[26:-1]) * 1024
                            else:
                                size += float(line[26:-1])
                            break
        if matching == 0:
            message = "Can't find"
            Msg().pkg_not_found("", ", ".join(self.binary), message, "\n")
        else:
            print("\n{0}Total found {1} matching packages.{2}".format(
                self.meta.color["GREY"], matching, self.meta.color["ENDC"]))
            unit = "Kb"
            if size > 1024:
                unit = "Mb"
                size = (size / 1024)
            print("{0}Size of installed packages {1} {2}.{3}\n".format(
                self.meta.color["GREY"], round(size, 2), unit,
                self.meta.color["ENDC"]))

    def display(self):
        """Print the Slackware packages contents
        """
        for pkg in self.binary:
            find = find_package(pkg + self.meta.sp, self.meta.pkg_path)
            if find:
                package = Utils().read_file(
                    self.meta.pkg_path + "".join(find[0]))
                print(package)
                print("")   # new line per file
            else:
                message = "Can't dislpay"
                if len(self.binary) > 1:
                    bol = eol = ""
                else:
                    bol = eol = "\n"
                Msg().pkg_not_found(bol, pkg, message, eol)

    def package_list(self, repo, INDEX, installed):
        """List with the installed packages
        """
        tty_size = os.popen("stty size", "r").read().split()
        row = int(tty_size[0]) - 2
        try:
            index, page, pkg_list = 0, row, []
            r = self.list_lib(repo)
            pkg_list = self.list_greps(repo, r)[0]
            print("")
            for pkg in sorted(pkg_list):
                if INDEX:
                    index += 1
                    pkg = self.list_color_tag(pkg)
                    print("{0}{1}:{2} {3}".format(
                        self.meta.color["GREY"], index,
                        self.meta.color["ENDC"], pkg))
                    if index == page:
                        read = raw_input("\nPress {0}Enter{1} to "
                                         "continue... ".format(
                                             self.meta.color["CYAN"],
                                             self.meta.color["ENDC"]))
                        if read in ["Q", "q"]:
                            break
                        print("")   # new line after page
                        page += row
                elif installed:
                    if self.list_of_installed(pkg):
                        print("{0}{1}{2}".format(self.meta.color["GREEN"], pkg,
                                                 self.meta.color["ENDC"]))
                else:
                    print(pkg)
            print("")   # new line at end
        except KeyboardInterrupt:
            print("")   # new line at exit
            sys.exit(0)

    def list_greps(self, repo, packages):
        """Grep packages
        """
        pkg_list, pkg_size = [], []
        for line in packages.splitlines():
            if repo == "sbo":
                if line.startswith("SLACKBUILD NAME: "):
                    pkg_list.append(line[17:].strip())
                    pkg_size.append("0 K")
            else:
                if line.startswith("PACKAGE NAME: "):
                    pkg_list.append(line[15:].strip())
                if line.startswith("PACKAGE SIZE (compressed): "):
                    pkg_size.append(line[26:].strip())
        if repo == "alien":
            return alien_filter(pkg_list, pkg_size)
        return pkg_list, pkg_size

    def list_lib(self, repo):
        """Return package lists
        """
        if repo == "sbo":
            if (os.path.isfile(
                    self.meta.lib_path + "{0}_repo/SLACKBUILDS.TXT".format(
                        repo))):
                packages = Utils().read_file(self.meta.lib_path + "{0}_repo/"
                                             "SLACKBUILDS.TXT".format(repo))
        else:
            if (os.path.isfile(
                    self.meta.lib_path + "{0}_repo/PACKAGES.TXT".format(repo))):
                packages = Utils().read_file(self.meta.lib_path + "{0}_repo/"
                                             "PACKAGES.TXT".format(repo))
        return packages

    def list_color_tag(self, pkg):
        """Tag with color installed packages
        """
        find = pkg + self.meta.sp
        if pkg.endswith(".txz") or pkg.endswith(".tgz"):
            find = pkg[:-4]
        if find_package(find, self.meta.pkg_path):
            pkg = "{0}{1}{2}".format(self.meta.color["GREEN"], pkg,
                                     self.meta.color["ENDC"])
        return pkg

    def list_of_installed(self, pkg):
        """Return installed packages
        """
        find = pkg + self.meta.sp
        if pkg.endswith(".txz") or pkg.endswith(".tgz"):
            find = pkg[:-4]
        if find_package(find, self.meta.pkg_path):
            return pkg


def alien_filter(packages, sizes):
    """This filter avoid list double packages from
    alien repository
    """
    cache, npkg, nsize = [], [], []
    for p, s in zip(packages, sizes):
        name = split_package(p)[0]
        if name not in cache:
            cache.append(name)
            npkg.append(p)
            nsize.append(s)
    return npkg, nsize
