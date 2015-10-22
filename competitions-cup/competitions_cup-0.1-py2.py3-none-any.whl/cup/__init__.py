# -*- coding: utf-8  -*-
"""Cup package."""

# Copyright (C) 2015 Alexander Jones
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import pkg_resources


class CupConfig(object):

    """Cup configuration singleton class."""

    created = False

    def __init__(self):
        """Constructor."""
        if CupConfig.created:
            raise RuntimeError
        CupConfig.created = True
        self._cup_types = {}
        for cup in pkg_resources.iter_entry_points(group='competitions.cup.types'):
            self._cup_types.update({cup.name: cup.load()})

    def cup(self, name):
        return self._cup_types[name]


config = CupConfig()
