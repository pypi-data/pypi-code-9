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

from flask import g, url_for
from . import TestCase
from .. import app
from ..models import (
    Graph, Person, RelationshipType, Relationship, Permission,
    PermissionLevel)


class GraphTestCase(TestCase):

    def setUp(self):
        super(GraphTestCase, self).setUp()
        self.graph = Graph(name="test")
        self.db.add(self.graph)
        self.db.commit()

    def test_copy_graph_with_center(self):
        graph2 = Graph(name="test2")
        self.db.add(graph2)
        self.db.flush()
        person = Person(graph_id=graph2.id, name="person")
        self.db.add(person)
        self.db.flush()
        graph2.center_id = person.id
        self.db.commit()
        self.graph.copy_from(graph2)
        self.assertEqual(len(self.graph.persons), 1)
        person2 = self.graph.persons[0]
        self.assertEqual(self.graph.center_id, person2.id)

    def test_copy_graph_without_center(self):
        graph2 = Graph(name="test2")
        self.db.add(graph2)
        self.db.flush()
        self.db.commit()
        self.graph.copy_from(graph2)
        self.assertIsNone(self.graph.center_id)
