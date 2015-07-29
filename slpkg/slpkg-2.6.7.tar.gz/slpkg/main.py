#!/usr/bin/python
# -*- coding: utf-8 -*-

# main.py file is part of slpkg.

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
import getpass

from load import Regex
from desc import PkgDesc
from messages import Msg
from auto_pkg import Auto
from config import Config
from checks import Updates
from queue import QueuePkgs
from repoinfo import RepoInfo
from repolist import RepoList
from repositories import Repo
from tracking import TrackingDeps
from blacklist import BlackList
from version import prog_version
from health import PackageHealth
from pkg_find import find_from_repos
from arguments import options, usage
from slpkg_update import it_self_update
from status_deps import DependenciesStatus

from init import (
    Update,
    Initialization,
    check_exists_repositories
)
from __metadata__ import MetaData as _meta_

from pkg.build import BuildPackage
from pkg.manager import PackageManager

from sbo.views import SBoNetwork
from sbo.check import sbo_upgrade
from sbo.slackbuild import SBoInstall

from slack.patches import Patches
from binary.check import pkg_upgrade
from binary.install import BinaryInstall


class ArgParse(object):

    def __init__(self, args):
        self.args = args
        self.meta = _meta_
        self.commands = [
            "update",
            "upgrade",
            "repo-add",
            "repo-remove",
            "repo-list",
            "repo-info",
            "update-slpkg",
            "health",
            "deps-status"
        ]

        # checking if repositories exists
        if len(self.args) > 1 and self.args[0] not in [
            "-h", "--help", "-v", "--version", "upgrade", "repo-list",
            "repo-add", "repo-remove", "update", "update-slpkg",
            "health", "-g", "--config"
        ]:
            check_exists_repositories()

    def help_version(self):
        """Help and version info
        """
        if (len(self.args) == 1 and self.args[0] in ["-h", "--help"] and
                self.args[1:] == []):
            options()
        elif (len(self.args) == 1 and self.args[0] in ["-v", "--version"] and
                self.args[1:] == []):
            prog_version()
        else:
            usage("")

    def command_update(self):
        """Update package lists repositories
        """
        if len(self.args) == 1 and self.args[0] == "update":
            Update().repository(only="")
        elif (len(self.args) == 2 and self.args[0] == "update" and
                self.args[1].startswith("--only=")):
            repos = self.args[1].split("=")[-1].split(",")
            for rp in repos:
                if rp not in self.meta.repositories:
                    repos.remove(rp)
            Update().repository(repos)
        else:
            usage("")

    def command_update_slpkg(self):
        """Slpkg it self update
        """
        if len(self.args) == 2 and self.args[0] == "update-slpkg":
            it_self_update()
        else:
            usage("")

    def command_repo_list(self):
        """Repositories list
        """
        if len(self.args) == 1 and self.args[0] == "repo-list":
            RepoList().repos()
        else:
            usage("")

    def command_repo_add(self):
        """Add custom repositories
        """
        if len(self.args) == 3 and self.args[0] == "repo-add":
            Repo().add(self.args[1], self.args[2])
        else:
            usage("")

    def command_repo_remove(self):
        """Remove custom repositories
        """
        if len(self.args) == 2 and self.args[0] == "repo-remove":
            Repo().remove(self.args[1])
        else:
            usage("")

    def command_upgrade(self):
        """Recreate repositories package lists
        """
        if len(self.args) == 1 and self.args[0] == "upgrade":
            Initialization(False).upgrade(only="")
        elif (len(self.args) == 2 and self.args[0] == "upgrade" and
                self.args[1].startswith("--only=")):
            repos = self.args[1].split("=")[-1].split(",")
            Initialization(False).upgrade(repos)
        else:
            usage("")

    def command_repo_info(self):
        """Repositories informations
        """
        if (len(self.args) == 2 and self.args[0] == "repo-info" and
                self.args[1] in RepoList().all_repos):
            del RepoList().all_repos
            RepoInfo().view(self.args[1])
        elif (len(self.args) > 1 and self.args[0] == "repo-info" and
                self.args[1] not in RepoList().all_repos):
            usage(self.args[1])
        else:
            usage("")

    def command_health(self):
        """Check package health
        """
        if len(self.args) == 1 and self.args[0] == "health":
            PackageHealth(mode="").test()
        elif (len(self.args) == 2 and self.args[0] == "health" and
                self.args[1] == "--silent"):
            PackageHealth(mode=self.args[1]).test()
        else:
            usage("")

    def command_deps_status(self):
        """Print dependencies status
        """
        if len(self.args) == 1 and self.args[0] == "deps-status":
            DependenciesStatus(image="").show()
        elif (len(self.args) == 2 and self.args[0] == "deps-status" and
                self.args[1].startswith("--graph=")):
            image = self.args[1].split("=")[1]
            DependenciesStatus(image).show()
        else:
            usage("")

    def auto_build(self):
        """Auto built tool
        """
        options = ["-a", "--autobuild"]
        if len(self.args) >= 3 and self.args[0] in options:
            BuildPackage(self.args[1], self.args[2:], self.meta.path).build()
        else:
            usage("")

    def pkg_list(self):
        """List of packages by repository
        """
        options = ["-l", "--list"]
        flag = ["--index", "--installed"]
        if (len(self.args) == 3 and self.args[0] in options and
                self.args[1] in self.meta.repositories):
            if self.args[2] == flag[0]:
                PackageManager(binary=None).package_list(self.args[1],
                                                         INDEX=True,
                                                         installed=False)
            elif self.args[2] == flag[1]:
                PackageManager(binary=None).package_list(self.args[1],
                                                         INDEX=False,
                                                         installed=True)
            else:
                usage("")
        elif (len(self.args) == 2 and self.args[0] in options and
                self.args[1] in self.meta.repositories):
            PackageManager(None).package_list(self.args[1], INDEX=False,
                                              installed=False)
        elif (len(self.args) > 1 and self.args[0] in options and
                self.args[1] not in self.meta.repositories):
            usage(self.args[1])
        else:
            usage("")

    def pkg_upgrade(self):
        """Check and upgrade packages by repository
        """
        options = ["-c", "--check"]
        flags = ["--upgrade", "--skip=", "--resolve-off"]
        flags, flag, skip = self.__pkg_upgrade_flags(flags)
        if (len(self.args) == 3 and self.args[0] in options and
                self.args[2] == flags[0] and
                self.args[1] in self.meta.repositories):
            if self.args[1] not in ["slack", "sbo"]:
                BinaryInstall(pkg_upgrade(self.args[1], skip),
                              self.args[1], flag).start(if_upgrade=True)
            elif self.args[1] == "slack":
                if self.meta.only_installed in ["on", "ON"]:
                    BinaryInstall(pkg_upgrade("slack", skip),
                                  "slack", flag).start(if_upgrade=True)
                else:
                    Patches(skip, flag).start()
            elif self.args[1] == "sbo":
                SBoInstall(sbo_upgrade(skip), flag).start(if_upgrade=True)
            else:
                usage(self.args[1])
        elif len(self.args) == 2 and self.args[0] in options:
            if self.args[1] == "ALL":
                Updates(repo="").ALL()
            else:
                Updates(self.args[1]).run()
        elif (len(self.args) >= 2 and self.args[0] in options and
                self.args[1] not in self.meta.repositories):
            usage(self.args[1])
        else:
            usage("")

    def __pkg_upgrade_flags(self, flags):
        """Manage flags for package upgrade option
        """
        flag = skip, i = "", 0
        if flags[0] in self.args:
            if flags[2] in self.args:
                flag = flags[2]
                index = self.args.index(flags[2])
                del self.args[index]
            for arg in self.args:
                if arg.startswith(flags[1]):
                    skip = Regex(self.args[i].split("=")[1]).get()
                    self.args.pop(i)
                i += 1
        return flags, flag, skip

    def pkg_install(self):
        """Install packages by repository
        """
        options = ["-s", "--sync"]
        flag = ""
        flags = ["--resolve-off"]
        if self.args[-1] in flags:
            flag = self.args[-1]
        if len(self.args) >= 3 and self.args[0] in options:
            if (self.args[1] in self.meta.repositories and
                    self.args[1] not in ["sbo"]):
                BinaryInstall(self.args[2:], self.args[1], flag).start(
                    if_upgrade=False)
            elif (self.args[1] == "sbo" and
                    self.args[1] in self.meta.repositories):
                SBoInstall(self.args[2:], flag).start(if_upgrade=False)
            else:
                usage(self.args[1])
        else:
            usage("")

    def pkg_tracking(self):
        """Tracking package dependencies
        """
        options = ["-t", "--tracking"]
        flag = ["--check-deps", "--graph="]
        if (len(self.args) == 3 and self.args[0] in options and
                self.args[1] in self.meta.repositories):
            TrackingDeps(self.args[2], self.args[1], flag="").run()
        elif (len(self.args) == 4 and self.args[0] in options and
                self.args[1] in self.meta.repositories and
                self.args[3] == flag[0]):
            TrackingDeps(self.args[2], self.args[1], flag[0]).run()
        elif (len(self.args) == 4 and self.args[0] in options and
                self.args[1] in self.meta.repositories and
                self.args[3].startswith(flag[1])):
            TrackingDeps(self.args[2], self.args[1], self.args[3]).run()
        elif (len(self.args) == 5 and self.args[0] in options and
                self.args[1] in self.meta.repositories and
                self.args[3] == flag[0] and self.args[4].startswith(flag[1])):
            TrackingDeps(self.args[2], self.args[1],
                         self.args[3] + self.args[4]).run()
        elif (len(self.args) > 1 and self.args[0] in options and
                self.args[1] not in self.meta.repositories):
            usage(self.args[1])
        else:
            usage("")

    def sbo_network(self):
        """View slackbuilds packages
        """
        options = ["-n", "--network"]
        if (len(self.args) == 2 and self.args[0] in options and
                "sbo" in self.meta.repositories):
            SBoNetwork(self.args[1]).view()
        else:
            usage("")

    def pkg_blacklist(self):
        """Manage blacklist packages
        """
        blacklist = BlackList()
        options = ["-b", "--blacklist"]
        flag = ["--add", "--remove"]
        command = ["list"]
        if (len(self.args) == 2 and self.args[0] in options and
                self.args[1] == command[0]):
            blacklist.listed()
        elif (len(self.args) > 2 and self.args[0] in options and
                self.args[-1] == flag[0]):
            blacklist.add(self.args[1:-1])
        elif (len(self.args) == 3 and self.args[0] in options and
                self.args[1] == "ALL" and self.args[-1] == flag[1]):
            blacklist.remove(blacklist.get_black())
        elif (len(self.args) > 2 and self.args[0] in options and
                self.args[-1] == flag[1]):
            blacklist.remove(self.args[1:-1])
        else:
            usage("")

    def pkg_queue(self):
        """Manage packages in queue
        """
        queue = QueuePkgs()
        options = ["-q", "--queue"]
        flag = ["--add", "--remove"]
        command = ["list", "build", "install", "build-install"]
        if (len(self.args) > 2 and self.args[0] in options and
                self.args[-1] == flag[0]):
            queue.add(self.args[1:-1])
        elif (len(self.args) == 3 and self.args[0] in options and
                self.args[1] == "ALL" and self.args[-1] == flag[1]):
            queue.remove(queue.packages())
        elif (len(self.args) > 2 and self.args[0] in options and
                self.args[-1] == flag[1]):
            queue.remove(self.args[1:-1])
        elif (len(self.args) == 2 and self.args[0] in options and
                self.args[1] == command[0]):
            queue.listed()
        elif (len(self.args) == 2 and self.args[0] in options and
                self.args[1] == command[1]):
            queue.build()
        elif (len(self.args) == 2 and self.args[0] in options and
                self.args[1] == command[2]):
            queue.install()
        elif (len(self.args) == 2 and self.args[0] in options and
                self.args[1] == command[3]):
            queue.build()
            queue.install()
        else:
            usage("")

    def bin_install(self):
        """Install Slackware binary packages
        """
        packages = self.args[1:]
        options = ["-i", "--installpkg"]
        flag = ""
        flags = [
            "--warn",
            "--md5sum",
            "--root",
            "--infobox",
            "--menu",
            "--terse",
            "--ask",
            "--priority",
            "--tagfile"
        ]
        if len(self.args) > 1 and self.args[0] in options:
            if self.args[1] in flags:
                flag = self.args[1]
                packages = self.args[2:]
            PackageManager(packages).install(flag)
        else:
            usage("")

    def bin_upgrade(self):
        """Install-upgrade Slackware binary packages
        """
        packages = self.args[1:]
        options = ["-u", "--upgradepkg"]
        flag = ""
        flags = [
            "--dry-run",
            "--install-new",
            "--reinstall",
            "--verbose"
        ]
        if len(self.args) > 1 and self.args[0] in options:
            if self.args[1] in flags:
                flag = self.args[1]
                packages = self.args[2:]
            PackageManager(packages).upgrade(flag)
        else:
            usage("")

    def bin_remove(self):
        """Remove Slackware packages
        """
        packages = self.args[1:]
        options = ["-r", "--removepkg"]
        additional_options = ["--check-deps"]
        flag = extra = ""
        flags = [
            "-warn",
            "-preserve",
            "-copy",
            "-keep"
        ]
        if len(self.args) > 1 and self.args[0] in options:
            if self.args[-1] == additional_options[0]:
                extra = additional_options[0]
                packages = self.args[1:-1]
            if self.args[1] in flags:
                flag = self.args[1]
                packages = self.args[2:]
            PackageManager(packages).remove(flag, extra)
        else:
            usage("")

    def bin_find(self):
        """Find installed packages
        """
        packages = self.args[1:]
        options = ["-f", "--find"]
        if len(self.args) > 1 and self.args[0] in options:
            PackageManager(packages).find()
        else:
            usage("")

    def pkg_desc(self):
        """Print slack-desc by repository
        """
        options = ["-p", "--desc"]
        flag = ["--color="]
        colors = ["red", "green", "yellow", "cyan", "grey"]
        if (len(self.args) == 3 and self.args[0] in options and
                self.args[1] in self.meta.repositories):
            PkgDesc(self.args[2], self.args[1], paint="").view()
        elif (len(self.args) == 4 and self.args[0] in options and
                self.args[3].startswith(flag[0])):
            tag = self.args[3][len(flag[0]):]
            if self.args[1] in self.meta.repositories and tag in colors:
                PkgDesc(self.args[2], self.args[1], tag).view()
            else:
                usage(self.args[1])
        elif (len(self.args) > 1 and self.args[0] in options and
                self.args[1] not in self.meta.repositories):
            usage(self.args[1])
        else:
            usage("")

    def pkg_find(self):
        """Find packages from all enabled repositories
        """
        packages = self.args[1:]
        options = ["-F", "--FIND"]
        if len(self.args) > 1 and self.args[0] in options:
            find_from_repos(packages)
        else:
            usage("")

    def pkg_contents(self):
        """Print packages contents
        """
        packages = self.args[1:]
        options = ["-d", "--display"]
        if len(self.args) > 1 and self.args[0] in options:
            PackageManager(packages).display()
        else:
            usage("")

    def congiguration(self):
        """Manage slpkg configuration file
        """
        options = ["-g", "--config"]
        command = ["print", "edit="]
        if (len(self.args) == 2 and self.args[0] in options and
                self.args[1].startswith(command[1])):
            editor = self.args[1][len(command[1]):]
            Config().edit(editor)
        elif (len(self.args) == 2 and self.args[0] in options and
                self.args[1] == (command[0])):
            Config().view()
        else:
            usage("")

    def auto_detect(self, args):
        """Check for already Slackware binary packages exist
        """
        if (not args[0].startswith("-") and args[0] not in self.commands and
                args[0].endswith(".tgz") or args[0].endswith(".txz")):
            packages, not_found = [], []
            for pkg in args:
                if pkg.endswith(".tgz") or pkg.endswith(".txz"):
                    if os.path.isfile(pkg):
                        packages.append(pkg)
                    else:
                        not_found.append(pkg)
            if packages:
                Auto(packages).select()
            if not_found:
                for ntf in not_found:
                    Msg().pkg_not_found("", ntf, "Not installed", "")
            sys.exit(0)


def main():

    Msg().s_user(getpass.getuser())
    args = sys.argv
    args.pop(0)

    argparse = ArgParse(args)

    if len(args) == 0:
        usage("")
        sys.exit(0)

    argparse.auto_detect(args)

    if len(args) == 2 and args[0] == "update" and args[1] == "slpkg":
        args[0] = "update-slpkg"

    arguments = {
        "-h": argparse.help_version,
        "--help": argparse.help_version,
        "-v": argparse.help_version,
        "--version": argparse.help_version,
        "update": argparse.command_update,
        "upgrade": argparse.command_upgrade,
        "update-slpkg": argparse.command_update_slpkg,
        "repo-list": argparse.command_repo_list,
        "repo-add": argparse.command_repo_add,
        "repo-remove": argparse.command_repo_remove,
        "repo-info": argparse.command_repo_info,
        "health": argparse.command_health,
        "deps-status": argparse.command_deps_status,
        "-a": argparse.auto_build,
        "--autobuild": argparse.auto_build,
        "-l": argparse.pkg_list,
        "--list": argparse.pkg_list,
        "-c": argparse.pkg_upgrade,
        "--check": argparse.pkg_upgrade,
        "-s": argparse.pkg_install,
        "--sync": argparse.pkg_install,
        "-t": argparse.pkg_tracking,
        "--tracking": argparse.pkg_tracking,
        "-n": argparse.sbo_network,
        "--netwotk": argparse.sbo_network,
        "-b": argparse.pkg_blacklist,
        "--blacklist": argparse.pkg_blacklist,
        "-q": argparse.pkg_queue,
        "--queue": argparse.pkg_queue,
        "-i": argparse.bin_install,
        "--installpkg": argparse.bin_install,
        "-u": argparse.bin_upgrade,
        "--upgradepkg": argparse.bin_upgrade,
        "-r": argparse.bin_remove,
        "--removepkg": argparse.bin_remove,
        "-f": argparse.bin_find,
        "--find": argparse.bin_find,
        "-F": argparse.pkg_find,
        "--FIND": argparse.pkg_find,
        "-p": argparse.pkg_desc,
        "--desc": argparse.pkg_desc,
        "-d": argparse.pkg_contents,
        "--display": argparse.pkg_contents,
        "-g": argparse.congiguration,
        "--config": argparse.congiguration
    }
    try:
        arguments[args[0]]()
    except KeyError:
        usage("")


if __name__ == "__main__":
    main()
