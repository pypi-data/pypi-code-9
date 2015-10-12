# -*- coding: utf-8  -*-
"""Match package."""

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


class MatchConfig(object):

    """Match configuration singleton class."""

    created = False

    def __init__(self):
        """Constructor."""
        if MatchConfig.created:
            raise RuntimeError
        MatchConfig.created = True
        self._base_matches = {}
        for match in pkg_resources.iter_entry_points(group='competitions.match.base'):
            self._base_matches.update({match.name: match.load()})
        self.base_match = 'competitions.simple'

    @property
    def base_match(self):
        return self._base_matches.get(self._base_match, None)

    @base_match.setter
    def base_match(self, match_def):
        self._base_match = match_def


config = MatchConfig()
