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
import argparse

# http://readthedocs.org/docs/nose/en/latest/testing_tools.html
from nose import tools as nt


class TestApiMain(unittest.TestCase):

    def get_api(self):
        from nexiles.tools.api import get_api

        api = get_api("http://example.com/Windchill", username="fred", password="kaputnik")
        assert api, "api is None"

        return api

    def test_get_api(self):
        api = self.get_api()

        self.assertEquals(api._store["append_slash"], False)
        self.assertEquals(api._store["base_url"], "http://example.com/Windchill/servlet/nexiles/tools/api/1.0")
        self.assertEquals(api._store["session"].auth, ("fred", "kaputnik"))

    def test_get_resource(self):
        from nexiles.tools.api import get_resource
        api = self.get_api()

        resource = get_resource(api, "documents")
        self.assertTrue(resource._store["base_url"].endswith("documents"))

        resource = get_resource(api, "document")
        self.assertTrue(resource._store["base_url"].endswith("documents"))


# vim: set ft=python ts=4 sw=4 expandtab :
