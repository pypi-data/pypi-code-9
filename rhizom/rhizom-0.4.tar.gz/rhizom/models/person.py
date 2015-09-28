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

from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship, object_session

from . import Base, DumpableMixin
from .relationship import Relationship


class Person(Base, DumpableMixin):

    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True)
    graph_id = Column(Integer,
        ForeignKey("graphs.id", ondelete="cascade", onupdate="cascade"),
        nullable=False)
    name = Column(Unicode(254), index=True)

    dump_attr = ("name",)

    def __repr__(self):
        return '<Person %r>' % (self.name)

    @property
    def relationships(self):
        targets = object_session(self).query(Person).join(
            Relationship, Person.id==Relationship.target_id
            ).filter(Relationship.source_id == self.id)
        sources = object_session(self).query(Person).join(
            Relationship, Person.id==Relationship.source_id
            ).filter(Relationship.target_id == self.id)
        return targets.union(sources).all()
