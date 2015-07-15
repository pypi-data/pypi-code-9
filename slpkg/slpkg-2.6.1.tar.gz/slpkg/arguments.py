#!/usr/bin/python
# -*- coding: utf-8 -*-

# arguments.py file is part of slpkg.

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


from repolist import RepoList
from __metadata__ import MetaData as _meta_


def header():
    """help header message"""
    print("\nslpkg - version {0} | Slackware release: {1}\n".format(
        _meta_.__version__, _meta_.slack_rel))


def options():
    """Slpkg is a user-friendly package manager for Slackware installations
                                                 _       _
                                             ___| |_ __ | | ____ _
                                            / __| | "_ \| |/ / _` |
                                            \__ \ | |_) |   < (_| |
                                            |___/_| .__/|_|\_\__, |
                                                  |_|        |___/

Commands:
   update, --only=[...]                     Run this command to update all
                                            the packages list.
   upgrade, --only=[...]                    Delete and recreate all packages
                                            lists.
   repo-add [repository name] [URL]         Add custom repository.
   repo-remove [repository]                 Remove custom repository.
   repo-list                                Print a list of all the
                                            repositories.
   repo-info [repository]                   Get information about a
                                            repository.
   update slpkg                             Upgrade the program directly from
                                            repository.

Optional arguments:
  -h, --help                                Print this help message and exit.
  -v, --version                             Print program version and exit.
  -a, --autobuild, [script] [source...]     Auto build SBo packages.
                                            If you already have downloaded the
                                            script and the source code you can
                                            build a new package with this
                                            command.
  -b, --blacklist, [package...] --add,      Manage packages in the blacklist.
      --remove, list                        Add or remove packages and print
                                            the list. Each package is added
                                            here will not be accessible by the
                                            program.
  -q, --queue, [package...] --add,          Manage SBo packages in the queue.
      --remove, list, build, install,       Add or remove and print the list
      build-install                         of packages. Build and then install
                                            the packages from the queue.
  -g, --config, print, edit=[editor]        Configuration file management.
                                            Print the configuration file or
                                            edit.
  -l, --list, [repository], --index,        Print a list of all available
      --installed                           packages repository, index or print
                                            only packages installed on the
                                            system.
  -c, --check, [repository], --upgrade,     Check, view and install updated
      --skip=[...] --resolve--off           packages from repositories.
  -s, --sync, [repository] [package...],    Sync packages. Install packages
      --resolve-off                         directly from remote repositories
                                            with all dependencies.
  -t, --tracking, [repository] [package]    Tracking package dependencies and
                                            print package dependenies tree with
                                            highlight if packages is installed.
  -p, --desc, [repository] [package],       Print description of a package
      --color=[]                            directly from the repository and
                                            change color text.
  -n, --network, [package]                  View a standard of SBo page in
                                            terminal and manage multiple options
                                            like reading, downloading, building
                                            installation, etc.
  -F, --FIND, [package...]                  Find packages from repositories and
                                            search at each enabled repository
                                            and prints results.
  -f, --find, [package...]                  Find and print installed packages
                                            reporting the size and the sum.
  -i, --installpkg, [options] [package...]  Installs single or multiple *.tgz
      options=[--warn, --md5sum, --root,    (or .tbz, .tlz, .txz) Slackware
      --infobox, --menu, --terse, --ask,    binary packages designed for use
      --priority, --tagfile]                with the Slackware Linux
                                            distribution onto your system.
  -u, --upgradepkg, [options] [package...]  Upgrade single or multiple Slackware
      options=[--dry-run, --install-new,    binary packages from an older
      --reinstall, --verbose]               version to a newer one.
  -r, --removepkg, [options] [package...],  Removes a previously installed
      --check-deps                          Slackware binary packages,
      options=[-warn, -preserve, -copy,     while writing a progress report
      -keep]                                to the standard output.
  -d, --display, [package...]               Display the installed packages
                                            contents and file list.

You can read more about slpkg from manpage or see examples from readme file.
Homepage: https://github.com/dslackw/slpkg
"""
    header()
    print(options.__doc__)


def usage(repo):
    """Usage: slpkg Commands:
             [update, --only=[...]] [upgrade, --only=[...]]
             [repo-add [repository name] [URL]]
             [repo-remove [repository]] [repo-list]
             [repo-info [repository]] [update [slpkg]]

             Optional arguments:
             [-h] [-v]
             [-a [script] [sources...]]
             [-b [package...] --add, --remove, list]
             [-q [package...] --add, --remove, list]
             [-q [build, install, build-install]]
             [-g [print, edit=[editor]]]
             [-l [repository], --index, --installed]
             [-c [repository], --upgrade, --skip=[...] --resolve-off]
             [-s [repository] [package...], --resolve-off]
             [-t [repository] [package]]
             [-p [repository] [package], --color=[]]
             [-n [SBo package]] [-F [...]] [-f [...]]
             [-i [options] [...]] [-u [options] [...]]
             [-r [options] [...], --check-deps] [-d [...]]
             """
    error_repo = ""
    if repo and repo not in _meta_.repositories:
        all_repos = RepoList().all_repos
        del RepoList().all_repos
        if repo in all_repos:
            error_repo = ("slpkg: error: repository '{0}' is not activated"
                          "\n".format(repo))
        else:
            error_repo = ("slpkg: error: repository '{0}' does not exist"
                          "\n".format(repo))
    header()
    print(usage.__doc__)
    print(error_repo)
    print("For more information try 'slpkg -h, --help' or view manpage\n")
