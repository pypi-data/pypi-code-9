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


__author__ = 'Alexander Rüedlinger'


class Device(object):

    def __init__(self, urn, location, descriptions):
        if descriptions is None or len(descriptions) == 0:
            raise AssertionError

        self._urn = urn
        self._location = location
        self._descriptions = descriptions

    @property
    def urn(self):
        return self._urn

    @property
    def location(self):
        return self._location

    @property
    def descriptions(self):
        return self._descriptions

    def __str__(self):
        return "{ urn: %s, url: %s }" % (self._urn, self._location)


class RemoteDevice(object):

    def __init__(self, urn, location, description):
        if description is None:
            raise AssertionError

        self._urn = urn
        self._location = location
        self._description = description

    @property
    def urn(self):
        return self._urn

    @property
    def location(self):
        return self._location

    @property
    def description(self):
        return self._description

    def __str__(self):
        return "{ urn: %s, url: %s }" % (self._urn, self._location)


class Description(object):

    def __init__(self, content_type='', content=''):
        self._content_type = content_type
        self._content = content

    @property
    def content(self):
        return self._content

    @property
    def content_type(self):
        return self._content_type