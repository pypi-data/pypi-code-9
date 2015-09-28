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


from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class DumpableMixin:
    """
    Allows conversion of a model object to a dict.
    The context of a given graph is assumed, thus the graph_id attribute is
    usually not included.
    """

    dump_attr = ()

    def as_dict(self):
        return dict((a, getattr(self, a)) for a in self.dump_attr)

    def from_dict(self, data):
        exclude_columns = [c.name for c in self.__table__.primary_key.columns]
        for fkc in self.__table__.foreign_key_constraints:
            exclude_columns.extend([c.name for c in fkc.columns])
        for attr in self.dump_attr:
            if attr in data and attr not in exclude_columns:
                setattr(self, attr, data[attr])


from .graph import Graph
from .person import Person
from .relationship import Relationship, RelationshipType
from .user import User, Permission, PermissionLevel
