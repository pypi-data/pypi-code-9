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
    PermissionLevel, User)


class GraphDataTestCase(TestCase):

    def test_siblings(self):
        graph = self.create_graph_and_login()
        person1 = Person(graph=graph, name="person1")
        person2 = Person(graph=graph, name="person2")
        person3 = Person(graph=graph, name="person3")
        self.db.add(person1)
        self.db.add(person2)
        reltype1 = RelationshipType(graph=graph, name="reltype1")
        reltype2 = RelationshipType(graph=graph, name="reltype2")
        self.db.add(reltype1)
        self.db.add(reltype2)
        rel1 = Relationship(graph=graph, source=person1, target=person2, type=reltype1)
        rel2 = Relationship(graph=graph, source=person1, target=person2, type=reltype2)
        rel3 = Relationship(graph=graph, source=person2, target=person3, type=reltype1)
        self.db.commit()
        response = self.client.get("/api/graph/1/data.js")
        data = json.loads(response.data)
        #print(data["links"])
        self.assertEqual(len(data["links"]), 3)
        self.assertIn(
            {'source': 0, 'target': 1, 'dotted': False,
             'sibling_id': 0, 'siblings': 2, 'css': 'reltype1'},
            data["links"])
        self.assertIn(
            {'source': 0, 'target': 1, 'dotted': False,
             'sibling_id': 1, 'siblings': 2, 'css': 'reltype2'},
            data["links"])
        self.assertIn(
            {'source': 1, 'target': 2, 'dotted': False,
             'sibling_id': 0, 'siblings': 1, 'css': 'reltype1'},
            data["links"])
