#!/usr/bin/python
# -*- coding: utf-8 -*

# installed.py file is part of slpkg.

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


from splitting import split_package
from __metadata__ import MetaData as _meta_

from pkg.find import find_package


class GetFromInstalled(object):
    """Find and return version and package name from
    already installed packages
    """
    def __init__(self, package):
        self.package = package
        self.meta = _meta_
        self.find = find_package(self.package + self.meta.sp,
                                 self.meta.pkg_path)

    def version(self):
        """Return version from installed packages
        """
        if self.find:
            if self.package == split_package(self.find[0])[0]:
                return self.meta.sp + split_package(self.find[0])[1]
        return ""

    def name(self):
        """Return installed package name
        """
        if self.find:
            return split_package(self.find[0])[0]
        return ""
