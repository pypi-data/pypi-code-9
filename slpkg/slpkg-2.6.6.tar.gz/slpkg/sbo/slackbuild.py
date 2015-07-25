#!/usr/bin/python
# -*- coding: utf-8 -*-

# slackbuild.py file is part of slpkg.

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

from slpkg.utils import Utils
from slpkg.messages import Msg
from slpkg.toolbar import status
from slpkg.log_deps import write_deps
from slpkg.blacklist import BlackList
from slpkg.downloader import Download
from slpkg.splitting import split_package
from slpkg.installed import GetFromInstalled
from slpkg.__metadata__ import MetaData as _meta_

from slpkg.pkg.find import find_package
from slpkg.pkg.build import BuildPackage
from slpkg.pkg.manager import PackageManager

from greps import SBoGrep
from remove import delete
from compressed import SBoLink
from dependency import Requires
from search import sbo_search_pkg


class SBoInstall(object):

    def __init__(self, slackbuilds, flag):
        self.slackbuilds = slackbuilds
        self.flag = flag
        self.meta = _meta_
        self.build_folder = self.meta.build_path
        self.unst = ["UNSUPPORTED", "UNTESTED"]
        self.master_packages = []
        self.deps = []
        self.dependencies = []
        self.package_not_found = []
        self.package_found = []
        self.deps_dict = {}
        self.answer = ""
        self.match = False
        Msg().reading()
        self.data = SBoGrep(name="").names()
        self.blacklist = BlackList().packages(pkgs=self.data, repo="sbo")

    def start(self, if_upgrade):
        try:
            tagc = ""
            count_ins = count_upg = count_uni = 0
            for _sbo in self.slackbuilds:
                status(0.03)
                if _sbo in self.data and _sbo not in self.blacklist:
                    sbo_deps = Requires(self.flag).sbo(_sbo)
                    self.deps += sbo_deps
                    self.deps_dict[_sbo] = self.one_for_all(sbo_deps)
                    self.package_found.append(_sbo)
                else:
                    self.package_not_found.append(_sbo)
            self.update_deps()
            if not self.package_found:
                self.match = True
                self.matching()
            self.master_packages, mas_src = self.sbo_version_source(
                self.package_found)
            Msg().done()
            if (self.meta.rsl_deps in ["on", "ON"] and
                    self.flag != "--resolve-off"):
                Msg().resolving()
            self.dependencies, dep_src = self.sbo_version_source(
                self.one_for_all(self.deps))
            if (self.meta.rsl_deps in ["on", "ON"] and
                    self.flag != "--resolve-off"):
                Msg().done()
            self.clear_masters()
            if self.package_found:
                print("\nThe following packages will be automatically "
                      "installed or upgraded \nwith new version:\n")
                self.top_view()
                Msg().upg_inst(if_upgrade)
                # view master packages
                for sbo, ar in zip(self.master_packages, mas_src):
                    tagc, count_ins, count_upg, count_uni = self.tag(
                        sbo, count_ins, count_upg, count_uni)
                    name = "-".join(sbo.split("-")[:-1])
                    self.view_packages(tagc, name, sbo.split("-")[-1],
                                       self.select_arch(ar))
                self._view_installing_for_deps()
                # view dependencies
                for dep, ar in zip(self.dependencies, dep_src):
                    tagc, count_ins, count_upg, count_uni = self.tag(
                        dep, count_ins, count_upg, count_uni)
                    name = "-".join(dep.split("-")[:-1])
                    self.view_packages(tagc, name, dep.split("-")[-1],
                                       self.select_arch(ar))
                count_total = (count_ins + count_upg + count_uni)
                print("\nInstalling summary")
                print("=" * 79)
                print("{0}Total {1} {2}.".format(
                    self.meta.color["GREY"], count_total,
                    Msg().pkg(count_total)))
                print("{0} {1} will be installed, {2} allready installed and "
                      "{3} {4}".format(count_uni, Msg().pkg(count_uni),
                                       count_ins, count_upg,
                                       Msg().pkg(count_upg)))
                print("will be upgraded.{0}\n".format(self.meta.color["ENDC"]))
                self._continue_to_install()
            else:
                Msg().not_found(if_upgrade)
        except KeyboardInterrupt:
            print("")   # new line at exit
            sys.exit(0)

    def update_deps(self):
        """Update dependencies dictionary with all package
        """
        for dep in self.one_for_all(self.deps):
            deps = Requires(self.flag).sbo(dep)
            self.deps_dict[dep] = self.one_for_all(deps)

    def _continue_to_install(self):
        """Continue to install ?
        """
        if self.master_packages and Msg().answer() in ["y", "Y"]:
            installs, upgraded = self.build_install()
            Msg().reference(installs, upgraded)
            write_deps(self.deps_dict)
            delete(self.build_folder)

    def _view_installing_for_deps(self):
        """View installing message for dependencies
        """
        if not self.match and self.dependencies:
            print("Installing for dependencies:")

    def clear_masters(self):
        """Clear master slackbuilds if already exist in dependencies
        or if added to install two or more times
        """
        self.master_packages = Utils().remove_dbs(self.master_packages)
        for mas in self.master_packages:
            if mas in self.dependencies:
                self.master_packages.remove(mas)

    def matching(self):
        """Return found matching SBo packages
        """
        for sbo in self.package_not_found:
            for pkg in self.data:
                if sbo in pkg and pkg not in self.blacklist:
                    self.package_found.append(pkg)

    def sbo_version_source(self, slackbuilds):
        """Create sbo name with version
        """
        sbo_versions, sources = [], []
        for sbo in slackbuilds:
            status(0.02)
            sbo_ver = "{0}-{1}".format(sbo, SBoGrep(sbo).version())
            sbo_versions.append(sbo_ver)
            sources.append(SBoGrep(sbo).source())
        return [sbo_versions, sources]

    def one_for_all(self, deps):
        """Because there are dependencies that depend on other
        dependencies are created lists into other lists.
        Thus creating this loop create one-dimensional list and
        remove double packages from dependencies.
        """
        requires, dependencies = [], []
        deps.reverse()
        requires = Utils().dimensional_list(deps)
        # Inverting the list brings the
        # dependencies in order to be installed.
        dependencies = Utils().remove_dbs(requires)
        return dependencies

    def top_view(self):
        """View top template
        """
        Msg().template(78)
        print("{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(
            "| Package", " " * 17,
            "New version", " " * 8,
            "Arch", " " * 4,
            "Build", " " * 2,
            "Repos", " " * 10,
            "Size"))
        Msg().template(78)

    def view_packages(self, *args):
        """:View slackbuild packages with version and arch
        args[0] package color
        args[1] package
        args[2] version
        args[3] arch
        """
        ver = GetFromInstalled(args[1]).version()
        print("  {0}{1}{2}{3} {4}{5} {6}{7}{8}{9}{10}{11:>11}{12}".format(
            args[0], args[1] + ver, self.meta.color["ENDC"],
            " " * (23-len(args[1] + ver)), args[2],
            " " * (18-len(args[2])), args[3],
            " " * (15-len(args[3])), "",
            "", "SBo", "", "")).rstrip()

    def tag(self, sbo, count_ins, count_upg, count_uni):
        """Tag with color green if package already installed,
        color yellow for packages to upgrade and color red
        if not installed.
        """
        # split sbo name with version and get name
        sbo_name = "-".join(sbo.split("-")[:-1])
        find = GetFromInstalled(sbo_name).name()
        if find_package(sbo, self.meta.pkg_path):
            paint = self.meta.color["GREEN"]
            count_ins += 1
        elif sbo_name == find:
            paint = self.meta.color["YELLOW"]
            count_upg += 1
        else:
            paint = self.meta.color["RED"]
            count_uni += 1
        return paint, count_ins, count_upg, count_uni

    def select_arch(self, src):
        """Looks if sources unsupported or untested
        from arch else select arch.
        """
        arch = os.uname()[4]
        if arch.startswith("i") and arch.endswith("86"):
            arch = "i486"
        for item in self.unst:
            if item in src:
                arch = item
        return arch

    def filenames(self, sources):
        """Return filenames from sources links
        """
        filename = []
        for src in sources:
            filename.append(src.split("/")[-1])
        return filename

    def search_in_tmp(self, prgnam):
        """Search for binary packages in /tmp directory
        """
        binary = []
        for search in find_package(prgnam, self.meta.output):
            if "_SBo" in search:
                binary.append(search)
        return binary

    def build_install(self):
        """Searches the package name and version in /tmp to
        install. If find two or more packages e.g. to build
        tag 2 or 3 will fit most.
        """
        slackbuilds = self.dependencies + self.master_packages
        installs, upgraded, = [], []
        if not os.path.exists(self.build_folder):
            os.makedirs(self.build_folder)
        os.chdir(self.build_folder)
        for sbo in slackbuilds:
            pkg = "-".join(sbo.split("-")[:-1])
            ver = sbo.split("-")[-1]
            prgnam = ("{0}-{1}".format(pkg, ver))
            sbo_file = "".join(find_package(prgnam, self.meta.pkg_path))
            src_link = SBoGrep(pkg).source().split()
            if sbo_file:
                Msg().template(78)
                Msg().pkg_found(pkg, split_package(sbo_file)[1])
                Msg().template(78)
            elif self.unst[0] in src_link or self.unst[1] in src_link:
                Msg().template(78)
                print("| Package {0} {1}{2}{3}".format(
                    sbo, self.meta.color["RED"], "".join(src_link),
                    self.meta.color["ENDC"]))
                Msg().template(78)
            else:
                sbo_url = sbo_search_pkg(pkg)
                sbo_link = SBoLink(sbo_url).tar_gz()
                script = sbo_link.split("/")[-1]
                dwn_srcs = sbo_link.split() + src_link
                Download(self.build_folder, dwn_srcs, repo="sbo").start()
                sources = self.filenames(src_link)
                BuildPackage(script, sources, self.build_folder).build()
                binary_list = self.search_in_tmp(prgnam)
                try:
                    binary = (self.meta.output + max(binary_list)).split()
                except ValueError:
                    Msg().build_FAILED(sbo_url, prgnam)
                    sys.exit(0)
                find = GetFromInstalled(pkg).name()
                if find == pkg:
                    print("[ {0}Upgrading{1} ] --> {2}".format(
                        self.meta.color["YELLOW"],
                        self.meta.color["ENDC"], sbo))
                    upgraded.append(prgnam)
                else:
                    print("[ {0}Installing{1} ] --> {2}".format(
                        self.meta.color["GREEN"], self.meta.color["ENDC"], sbo))
                    installs.append(prgnam)
                PackageManager(binary).upgrade(flag="--install-new")
        return installs, upgraded
