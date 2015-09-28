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

from __future__ import unicode_literals, print_function

import re

from sqlalchemy import Boolean, Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship, object_session
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.sql.expression import false

from . import Base, DumpableMixin


class Relationship(Base, DumpableMixin):

    __tablename__ = "relationships"
    __table_args__ = (
        ForeignKeyConstraint(
            ['graph_id', 'type_name'],
            ['relationship_types.graph_id', 'relationship_types.name'],
            ondelete="cascade", onupdate="cascade"
        ),
    )

    source_id = Column(Integer,
        ForeignKey("persons.id", ondelete="cascade", onupdate="cascade"),
        primary_key=True)
    target_id = Column(Integer,
        ForeignKey("persons.id", ondelete="cascade", onupdate="cascade"),
        primary_key=True)
    type_name = Column(Unicode(32), primary_key=True)
    graph_id = Column(Integer, ForeignKey("graphs.id"))
    dotted = Column(Boolean, server_default=false(), nullable=False)
    type = relationship("RelationshipType")
    source = relationship("Person", foreign_keys=[source_id])
    target = relationship("Person", foreign_keys=[target_id])

    dump_attr = ("source_id", "target_id", "type_name", "dotted")

    def __repr__(self):
        return '<Relationship %r - %r (%r)>' % (
                self.source_id, self.target_id, self.type)


class RelationshipType(Base, DumpableMixin):

    __tablename__ = "relationship_types"

    graph_id = Column(Integer,
        ForeignKey("graphs.id", ondelete="cascade", onupdate="cascade"),
        primary_key=True, nullable=False)
    name = Column(Unicode(32), primary_key=True, nullable=False)
    color = Column(Unicode(32))

    dump_attr = ("name", "color")

    @property
    def cssname(self):
        return re.sub('[^a-z0-9-]', '', self.name.lower())

    @property
    def rel_count(self):
        return object_session(self).query(Relationship).filter_by(
            graph_id=self.graph_id, type_name=self.name).count()

    def __repr__(self):
        return '<RelationshipType %r>' % self.name
