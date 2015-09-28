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

import os
import unittest
import tempfile

from .. import app
from ..database import init_db, get_session
from ..models import Graph, User, Permission, PermissionLevel

class TestCase(unittest.TestCase):

    def setUp(self):
        self._db_fd, self._db_filename = tempfile.mkstemp(
            prefix="rhizom-tests-", suffix=".db")
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + self._db_filename
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        init_db(app.config['SQLALCHEMY_DATABASE_URI'])
        self.db = get_session(app.config['SQLALCHEMY_DATABASE_URI'])

    def tearDown(self):
        self.db.close()
        os.close(self._db_fd)
        os.unlink(self._db_filename)

    def create_graph_and_login(self, graph_name="test"):
        # Create a graph, a user with admin permissions on it, and log it it.
        graph = Graph(name=graph_name)
        self.db.add(graph)
        self.db.commit()
        self.login()
        user = self.db.query(User).get("user@example.com")
        self.db.add(Permission(
            graph_id=graph.id, user_email=user.email,
            level=PermissionLevel.admin.value))
        self.db.commit()
        return graph

    def login(self, email=None):
        if email is None:
            email = "user@example.com"
        return self.client.post('/login', data={"email": email},
                                follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)
