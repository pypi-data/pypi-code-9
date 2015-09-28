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

from enum import IntEnum
from flask.ext.login import UserMixin
from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship, object_session
from sqlalchemy.orm.exc import NoResultFound

from . import Base, DumpableMixin
from .. import app


class User(Base, UserMixin, DumpableMixin):

    __tablename__ = 'users'

    email = Column(Unicode(120), primary_key=True)
    name = Column(Unicode(254))
    locale = Column(Unicode(10))
    permissions = relationship("Permission",
        backref="user", cascade="all, delete-orphan", passive_deletes=True)

    dump_attr = ("email", "name")

    def __repr__(self):
        return '<User %r>' % (self.email)

    def get_id(self):
        return self.email

    def has_perm(self, graph, level):
        if self.is_master:
            return True
        current_level = self.perm_for(graph)
        if current_level is None:
            return False
        return current_level >= getattr(PermissionLevel, level)

    @property
    def is_master(self):
        return self.email in app.config.get("ADMINS", [])

    def perm_for(self, graph):
        try:
            level = object_session(self).query(Permission.level
                ).with_parent(self).filter_by(
                graph_id=graph.id).one().level
        except NoResultFound:
            return None
        return PermissionLevel(level)


class Permission(Base, DumpableMixin):

    __tablename__ = 'permissions'

    graph_id = Column(Integer,
        ForeignKey("graphs.id", ondelete="cascade", onupdate="cascade"),
        primary_key=True)
    user_email = Column(Unicode(120),
        ForeignKey("users.email", ondelete="cascade", onupdate="cascade"),
        primary_key=True)
    level = Column(Integer)

    @property
    def level_as_string(self):
        return PermissionLevel(self.level).name

    def as_dict(self):
        return {
            "email": self.user_email,
            "level": self.level_as_string,
        }

    def from_dict(self, data):
        self.level = PermissionLevel[data["level"]].value


class PermissionLevel(IntEnum):
    view   = 1
    edit   = 2
    admin  = 3
