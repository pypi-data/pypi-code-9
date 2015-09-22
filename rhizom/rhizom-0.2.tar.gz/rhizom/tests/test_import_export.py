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


class ImportExportTestCase(TestCase):

    def test_import_export(self):
        graph = Graph(name="test")
        self.db.add(graph)
        self.db.commit()
        data = {
            "graph": {
                "name": "different name",
                "anonymous": True,
                "center_id": 2,
            },
            "persons": {
                "1": {"name": "person1"},
                "2": {"name": "person2"},
                "3": {"name": "person3"},
            },
            "relationships": [
                {"source_id": 1,
                 "target_id": 2,
                 "type_name": "type1",
                 "dotted": False, },
                {"source_id": 2,
                 "target_id": 3,
                 "type_name": "type2",
                 "dotted": True, },
            ],
            "relationship_types": [
                {"name": "type1", "color": "#0000FF", },
                {"name": "type2", "color": "#FF0000", },
            ],
            "permissions": [
                {"email": "user1@example.com", "level": "admin"},
                {"email": "user2@example.com", "level": "edit"},
                {"email": "user3@example.com", "level": "view"},
            ],
        }
        with app.test_request_context('/import'):
            app.preprocess_request()
            graph_in_context = g.db.query(Graph).get(graph.id)
            graph_in_context.import_dict(data)
            g.db.commit()
        self.db.refresh(graph) # change was done in a different session
        self.assertEqual(graph.name, "different name")
        self.assertTrue(graph.anonymous)
        persons = self.db.query(Person).filter_by(
            graph_id=graph.id).order_by(Person.name)
        self.assertEqual([p.name for p in persons],
                         ["person1", "person2", "person3"])
        person1 = self.db.query(Person).filter_by(name="person1").one()
        person2 = self.db.query(Person).filter_by(name="person2").one()
        person3 = self.db.query(Person).filter_by(name="person3").one()
        self.assertEqual(graph.center_id, person2.id)
        relationship_types = self.db.query(RelationshipType).filter_by(
            graph_id=graph.id).order_by(RelationshipType.name)
        self.assertEqual(
            [(rt.name, rt.color) for rt in relationship_types],
            [("type1", "#0000FF"), ("type2", "#FF0000")]
            )
        relationships = self.db.query(Relationship).filter_by(
            graph_id=graph.id).order_by(Relationship.source_id)
        self.assertEqual(
            [(r.source_id, r.target_id, r.type_name, r.graph_id, r.dotted)
             for r in relationships],
            [(person1.id, person2.id, "type1", graph.id, False),
             (person2.id, person3.id, "type2", graph.id, True)],
            )
        permissions = self.db.query(Permission).filter_by(
            graph_id=graph.id).order_by(Permission.user_email)
        self.assertEqual(
            [(p.user_email, p.level) for p in permissions],
            [("user1@example.com", PermissionLevel.admin.value),
             ("user2@example.com", PermissionLevel.edit.value),
             ("user3@example.com", PermissionLevel.view.value)]
            )

    def test_export_view_name_nonascii(self):
        graph = self.create_graph_and_login(graph_name="éléphant")
        response = self.client.get("/api/graph/1/export/graph.json")
        self.assertEqual(response.headers["Content-Disposition"],
            "attachment; filename*=UTF-8''%C3%A9l%C3%A9phant.json")
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(json.loads(response.data)["graph"]["name"], "éléphant")
