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
from sqlalchemy.orm.exc import NoResultFound
from . import TestCase
from .. import app
from ..models import (
    Graph, Person, RelationshipType, Relationship, Permission,
    PermissionLevel)


class AdminViewTestCase(TestCase):

    def setUp(self):
        super(AdminViewTestCase, self).setUp()
        self.graph = self.create_graph_and_login()
        self.db.commit()

    def test_admin_perm_add(self):
        url = '/graph/%d/admin' % self.graph.id
        response = self.client.post(url, data={
                "formname": "permissions",
                "action": "add",
                "newaccess-email": "newuser@example.com",
                "newaccess-level": "1",
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "http://localhost" + url)
        self.assertEqual(len(self.graph.permissions), 2)
        newperm = [ p for p in self.graph.permissions
                    if p.user_email == "newuser@example.com" and p.level == 1 ]
        self.assertEqual(len(newperm), 1)

    def test_admin_perm_edit(self):
        url = '/graph/%d/admin' % self.graph.id
        response = self.client.post(url, data={
                "formname": "permissions",
                "action": "edit",
                "email": "user@example.com",
                "level": "2",
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"status": "OK"})
        self.db.refresh(self.graph)
        self.assertEqual(len(self.graph.permissions), 1)
        self.assertEqual(
            [(p.user_email, p.level) for p in self.graph.permissions],
            [("user@example.com", 2)])
