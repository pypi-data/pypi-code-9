# -*- coding: utf-8 -*-
#
# Copyright (c) nexiles GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'


import unittest

# http://readthedocs.org/docs/nose/en/latest/testing_tools.html
from nose import tools as nt

from nexiles.tools.api.query import query


class Mock(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)


class MockAPI(Mock):
    def get(self, **kw):
        self._get_args = kw
        return self._get_result

    def __getattr__(self, key):
        self._get_resource = key
        return self


class TestQuery(unittest.TestCase):

    def get_api(self, results=None):
        if results is None:
            results = {"items": [], "count": 0}
        return MockAPI(_get_result=results)

    def test_query_default_type(self):
        mock_api = self.get_api()
        query(mock_api)
        nt.eq_(mock_api._get_resource, "documents")

    def test_query_args(self):
        mock_api = self.get_api()
        query(mock_api, limit=10, name="foo")
        nt.eq_(mock_api._get_args, {"limit": 10, "name": "foo"})

    def test_query_result(self):
        mock_api = self.get_api({"items": ["foo"]})
        nt.eq_(query(mock_api, limit=10, name="foo"), ["foo"])



# vim: set ft=python ts=4 sw=4 expandtab :
