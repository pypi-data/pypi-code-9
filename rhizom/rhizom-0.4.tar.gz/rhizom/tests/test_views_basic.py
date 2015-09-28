# -*- coding: utf-8 -*-
"""
Rhizom - Relationship grapher

Copyright (C) 2015  Aurelien Bompard <aurelien@bompard.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import absolute_import, unicode_literals, print_function

import json

from flask import g, url_for
from . import TestCase
from .. import app
from ..models import (
    Graph, Person, RelationshipType, Relationship, Permission,
    PermissionLevel)


class ViewsBasicTestCase(TestCase):

    def setUp(self):
        super(ViewsBasicTestCase, self).setUp()
        self.graph = self.create_graph_and_login()
        self.db.commit()

    def _test_view(self, url):
        #with app.test_request_context('/'):
        #    url = url_for(name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        return response

    def test_index(self):
        self._test_view('/')

    def test_graph(self):
        self._test_view('/graph/%d' % self.graph.id)

    def test_data(self):
        response = self._test_view(
            '/api/graph/%d/data.js' % self.graph.id)
        self.assertEqual(response.headers["Content-Type"], "application/json")

    def test_edit(self):
        self._test_view('/graph/%d/edit' % self.graph.id)

    def test_admin(self):
        self._test_view('/graph/%d/admin' % self.graph.id)

    def test_profile(self):
        self._test_view('/profile')

    def test_export_graph(self):
        response = self._test_view(
            '/api/graph/%d/export/graph.json' % self.graph.id)
        self.assertEqual(response.headers["Content-Type"], "application/json")

    def test_import_graph(self):
        data = {
            "graph": {},
            "relationship_types": [],
            "persons": {},
            "relationships": [],
        }
        response = self.client.post('/api/graph/%d/import' % self.graph.id,
            data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location,
                         'http://localhost/graph/%d' % self.graph.id)

    def test_as_svg(self):
        response = self.client.post('/api/graph/%d/export/graph.svg'
            % self.graph.id, data={'svg': '<svg></svg>'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "image/svg+xml; charset=utf-8")
        self.assertIn("<style>", response.data)
        self.assertIn("</style>", response.data)
        self.assertIn(".node circle", response.data)
