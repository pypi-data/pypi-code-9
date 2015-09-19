#!/usr/bin/env python
# -*- coding: utf-8 -*-

# main.py is part file of self.remove.

# Copyright 2015  Dimitris Zlatanidis  <d.zlatanidis@gmail.com>
# All rights reserved.

# dpline is tool to remove duplicate lines from file

# https://github.com/dslackw/self.remove

# Alarm is free software: you can redistribute it and/or modify
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


__prog__ = "dpline"
__author__ = "dslackw"
__version_info__ = (1, 3)
__version__ = "{0}.{1}".format(*__version_info__)
__license__ = "GNU General Public License v3 (GPLv3)"
__email__ = "d.zlatanidis@gmail.com"


class dpLine(object):
    """dpline is tool to remove duplicate lines from file"""

    def __init__(self):
        self.options = [
            "-h", "--help",
            "-v", "--version",
            "-d", "--display",
            "-p", "--preview"
        ]
        self.flags = [
            "--ignore-blank",
            "--case-ins",
            "--number"
        ]

    def remove(self):
        """Remove duplicate lines from text files"""
        num, sp, newfile = 0, "", []
        if os.path.isfile(self.filename):
            with open(self.filename, "r") as r:
                oldfile = r.read().splitlines()
                for line in oldfile:
                    if self.number:
                        num += 1
                        sp = ": "
                    if self.case_ins:
                        line = line.lower()
                    if self.ignore_blank and not line:
                        newfile.append(line)
                    elif line not in newfile:
                        newfile.append(line)
                    else:
                        if (self.args[0] in self.options[4:5] or
                                self.args[0] in self.options[6:7]):
                            if num == 0:
                                num = str()
                            print("{0}{1}{2}".format(num, sp, line))
            if self.args[0] not in self.options[6:7]:
                with open(self.filename, "w") as w:
                    for line in newfile:
                        w.write(line + "\n")
        else:
            self.not_access()

    def arguments(self, args):
        """Control arguments"""
        self.args = args
        self.manage_flags()
        self.filename = self.args[0]
        if len(self.args) == 1 and self.args[0] in self.options[:2]:
            print(self.help.__doc__)
        elif len(self.args) == 1 and self.args[0] in self.options[2:4]:
            self.version()
        elif len(self.args) == 2 and self.args[0] in self.options[4:5]:
            self.filename = self.args[1]
            self.remove()
        elif len(self.args) == 2 and self.args[0] in self.options[6:7]:
            self.filename = self.args[1]
            self.remove()
        elif len(self.args) == 1:
            if os.path.isfile(self.args[0]):
                self.remove()
            else:
                self.not_access()
        else:
            self.usage()

    def manage_flags(self):
        """Manage flags"""
        self.ignore_blank = False
        self.case_ins = False
        self.number = False
        for n in range(0, len(self.flags)):
            if len(self.args) >= 2:
                if self.args[-1] == self.flags[0]:
                    self.ignore_blank = True
                    index = self.args.index(self.args[-1])
                    del self.args[index]
                if self.args[-1] == self.flags[1]:
                    self.case_ins = True
                    index = self.args.index(self.args[-1])
                    del self.args[index]
                if self.args[-1] == self.flags[2]:
                    self.number = True
                    index = self.args.index(self.args[-1])
                    del self.args[index]
            del n

    def not_access(self):
        """Cannot access message and exit"""
        sys.exit("%s: cannot access %s: No such file" % (
            __prog__, self.filename))

    def help(self):
        """Usage: dpline [OPTION] <file> [--ignore-blank, [--case-ins],
                              [--number]]

dpline is tool to remove duplicate lines from file

Optional arguments:
  -h, --help          Print this help message and exit
  -v, --version       Print program version and exit
  -d, --display       Display removed lines
  -p, --preview       Preview duplicate lines before removal
  --ignore-blank      Ignore blank lines from remove
  --case-ins          Matching upper- and lowercase letters
  --number            View duplicate line number
    """

    def usage(self):
        """Usage message and exit"""
        sys.exit("Usage: dpline [OPTION] <file> [--ignore-blank, "
                 "[--case-ins], [--number]]"
                 "\n\nType dpline --help to see a list of all options")

    def version(self):
        """Print version and exit"""
        sys.exit("%s %s" % (__prog__, __version__))


def main():
    args = sys.argv
    args.pop(0)
    dpLine().arguments(args)

if __name__ == "__main__":
    main()
