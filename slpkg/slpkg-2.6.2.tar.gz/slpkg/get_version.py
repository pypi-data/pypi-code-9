#!/usr/bin/python
# -*- coding: utf-8 -*

# get_installed_version.py file is part of slpkg.

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


def get_installed_version(package):
    """Get version from installed packages
    """
    find = find_package(package + _meta_.sp, _meta_.pkg_path)
    if find:
        name = split_package(find[0])[0]
        if package == name:
            return _meta_.sp + split_package(find[0])[1]
    return ""
