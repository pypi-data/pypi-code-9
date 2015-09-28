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

from flask import g
from sqlalchemy import Column, Integer, Unicode, Boolean, ForeignKey
from sqlalchemy.orm import relationship, object_session
from sqlalchemy.sql.expression import false
from sqlalchemy.orm.exc import NoResultFound

from . import Base, DumpableMixin
from .person import Person
from .relationship import Relationship, RelationshipType
from .user import Permission, User
from ..database import get_or_create


class Graph(Base, DumpableMixin):

    __tablename__ = 'graphs'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(254), index=True)
    anonymous = Column(Boolean, server_default=false(), nullable=False)
    center_id = Column(Integer, nullable=True)
    persons = relationship("Person", backref="graph",
        cascade="all, delete-orphan", passive_deletes=True,
        foreign_keys="[Person.graph_id]")
    relationships = relationship("Relationship", backref="graph", viewonly=True)
    relationship_types = relationship("RelationshipType",
        backref="graph", cascade="all, delete-orphan", passive_deletes=True)
    permissions = relationship("Permission",
        backref="graph", cascade="all, delete-orphan")

    dump_attr = ("name", "anonymous", "center_id")


    @property
    def center(self):
        if self.center_id is None:
            return None
        return object_session(self).query(Person).get(self.center_id)

    @center.setter
    def center(self, person):
        if person is None:
            self.center_id = None
        else:
            db = object_session(self)
            self.center_id = db.query(Person).get(person.id).id

    def copy_from(self, graph):
        db = object_session(self)
        for perm in db.query(Permission).filter_by(graph_id=graph.id):
            db.add(Permission(graph_id=self.id,
                user_email=perm.user_email, level=perm.level))
        for person in db.query(Person).filter_by(graph_id=graph.id):
            db.add(Person(graph_id=self.id, name=person.name))
        for reltype in db.query(RelationshipType).filter_by(graph_id=graph.id):
            db.add(RelationshipType(graph_id=self.id,
                name=reltype.name, color=reltype.color))
        db.flush()
        self.anonymous = graph.anonymous
        if graph.center_id is not None:
            center = db.query(Person).filter_by(
                graph_id=self.id, name=graph.center.name).one()
            self.center_id = center.id
        for rel in db.query(Relationship).filter_by(graph_id=graph.id):
            source = db.query(Person).filter_by(
                graph_id=self.id, name=rel.source.name).one()
            target = db.query(Person).filter_by(
                graph_id=self.id, name=rel.target.name).one()
            db.add(Relationship(graph_id=self.id,
                source=source, target=target, type_name=rel.type_name))

    def export_dict(self, with_perms=False):
        data = {
            "graph": self.as_dict(),
            "relationship_types": [],
            "persons": {},
            "relationships": [],
        }
        for reltype in self.relationship_types:
            data["relationship_types"].append(reltype.as_dict())
        for person in self.persons:
            data["persons"][person.id] = person.as_dict()
        for rel in self.relationships:
            data["relationships"].append(rel.as_dict())
        if with_perms:
            data["permissions"] = []
            for perm in self.permissions:
                data["permissions"].append(perm.as_dict())
        return data

    def import_dict(self, data):
        self.from_dict(data["graph"])
        for reltype_data in data["relationship_types"]:
            reltype = get_or_create(RelationshipType,
                graph_id=self.id, name=reltype_data["name"])
            reltype.from_dict(reltype_data)
        for person_id_orig in sorted(data["persons"], key=int):
            person_data = data["persons"][person_id_orig]
            person = get_or_create(Person,
                graph_id=self.id, name=person_data["name"])
            person.from_dict(person_data)
        if data["graph"].get("center_id"):
            center_id = data["graph"]["center_id"]
            center_name = data["persons"][str(center_id)]["name"]
            center = g.db.query(Person).filter_by(
                graph_id=self.id, name=center_name).one()
            self.center_id = center.id
        for rel_data in data["relationships"]:
            source_name = data["persons"][str(rel_data["source_id"])]["name"]
            target_name = data["persons"][str(rel_data["target_id"])]["name"]
            source = g.db.query(Person).filter_by(
                graph_id=self.id, name=source_name).one()
            target = g.db.query(Person).filter_by(
                graph_id=self.id, name=target_name).one()
            rel = get_or_create(Relationship,
                graph_id=self.id, source_id=source.id, target_id=target.id,
                type_name=rel_data["type_name"])
            rel.from_dict(rel_data)
        if "permissions" in data:
            for perm_data in data["permissions"]:
                try:
                    perm = g.db.query(Permission).filter_by(
                        graph_id=self.id, user_email=perm_data["email"]).one()
                except NoResultFound:
                    user = get_or_create(User, email=perm_data["email"])
                    perm = Permission(graph_id=self.id, user_email=user.email)
                    g.db.add(perm)
                perm.from_dict(perm_data)
