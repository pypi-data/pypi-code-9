#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Yadp  - Yet Another Discovery Protocol
# Copyright (C) 2015  Alexander Rüedlinger
#
# This file is part of Yadp.
#
# Yadp is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Yadp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Yadp.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

__author__ = 'Alexander Rüedlinger'

import re


class URN(object):

    def __init__(self, urn):
        self._urn_str = urn
        self._urn_parts = urn.split(":")

    def is_valid(self):
        return len(self._urn_parts) >= 3 and self._urn_parts[0].upper() == "URN"

    def parts(self):
        return self._urn_parts

    def nss(self):
        return ":".join(self._urn_parts[2::])

    def nss_parts(self):
        return self._urn_parts[2::]

    def nid(self):
        return self._urn_parts[1]


class URNPattern(URN):

    def __init__(self, urn):
        super(URNPattern, self).__init__(urn)

    def match(self, urn):
        if self.is_valid():
            if self.is_questionmark():
                return self._match_questionmark(urn)
            elif self.is_regex():
                return self._match_regex(urn)
            elif self.is_star():
                return self._match_star(urn)
            else:
                return self._match_perfect(urn)

        else:
            return False

    def _match_perfect(self, urn):
        return self.nid() == urn.nid() and self.nss_parts() == urn.nss_parts()

    def _match_regex(self, urn):
        if urn.nid() != self.nid():
            return True

        if len(urn.nss_parts()) == len(self.nss_parts()):
            if urn.nss_parts()[0:-1] == self.nss_parts()[0:-1]:
                nss = urn.nss_parts()[-1]
            else:
                return False
        elif len(urn.nss_parts()) > len(self.nss_parts()):
            nss = urn.nss()
        else:
            return False

        regex_str = self._regex_str()
        p = re.compile(regex_str)

        return p.search(nss) is not None

    def _match_star(self, urn):
        if urn.nid() != self.nid():
            return False

        # pattern is longer than the urn
        if len(urn.nss_parts()) < len(self.nss_parts()):
            return False

        index = self.nss_parts().index('*')
        return urn.nss_parts()[0:index] == self.nss_parts()[0:-1]

    def _match_questionmark(self, urn):
        if urn.nid() != self.nid():
            return False

        # pattern length is not the same as the urn length
        if len(urn.nss_parts()) != len(self.nss_parts()):
            return False

        return urn.nss_parts()[0:-1] == self.nss_parts()[0:-1]

    def _regex_str(self):
        # last element of nss_parts() is the regex
        #  but is encapsulated in /regex/ so we need to get rid of the first and last char
        return self.nss_parts()[-1][1:-1]

    def is_regex(self):
        """
        urn:nid:nss1:/regex/
        """
        nss_parts = self.nss_parts()[-1]
        if len(nss_parts) >= 2:
            return nss_parts[-1][0] == '/' and nss_parts[-1][-1] == '/'
        else:
            return False

    def is_star(self):
        """
        urn:nid:nss1:nss2:*
        """
        return self.nss_parts()[-1] == '*'

    def is_questionmark(self):
        """
        urn:nid:nss1:nss2:?
        """
        return self.nss_parts()[-1] == '?'


class URNMatcher(object):

    def __init__(self):
        pass

    def match(self, urn_str, urn_pattern):
        urn = URN(urn_str)
        if not urn.is_valid():
            return False

        return URNPattern(urn_pattern).match(urn)
