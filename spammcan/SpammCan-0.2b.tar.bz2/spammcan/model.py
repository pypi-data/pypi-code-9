from datetime import datetime

import pkg_resources
pkg_resources.require("SQLAlchemy>=0.4.0")

from turbogears.database import mapper, metadata, session
# import some basic SQLAlchemy classes for declaring the data model
# (see http://www.sqlalchemy.org/docs/04/ormtutorial.html)
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relation
# import some datatypes for table columns from SQLAlchemy
# (see http://www.sqlalchemy.org/docs/04/types.html for more)
from sqlalchemy import String, Unicode, Integer, DateTime
from turbogears import identity


# your data tables
paste_table = Table('paste', metadata,
    Column('guid', String(32), primary_key=True),
    Column('title', Unicode(100)),
    Column('code', Unicode(10000)),
    Column('format_id', ForeignKey('format.name')),
    Column('creator', String(32)),
    Column('created', DateTime, nullable=False, default=datetime.now),
    Column('last_access', DateTime, nullable=False, default=datetime.now)
)

format_table = Table('format', metadata,
    Column('name', String(20), primary_key=True),
    Column('display_name', Unicode(20))
)

style_table = Table('style', metadata,
    Column('name', String(20), primary_key=True),
    Column('display_name', Unicode(20))
)

# your model classes
class Paste(object):
    @classmethod
    def by_guid(self, guid):
        """Look up paste instance by given GUID."""
        return cls.query.get(guid)

    def __repr__(self):
        return "<Paste guid=%r title=%r>" % (self.guid, self.title)

class Format(object):
    @classmethod
    def options(cls):
        """Return all Format instances as an iterator yielding 2-item tuples."""
        return ((f.name, f.display_name)
            for f in cls.query().order_by('display_name'))

    def __str__(self):
        return "%s (%s)" % (self.display_name, self.name)

class Style(object):
    @classmethod
    def options(cls):
        """Return all Style instances as an iterator yielding 2-item tuples."""
        return ((s.name, s.display_name)
            for s in cls.query().order_by('display_name'))

    def __str__(self):
        return "%s (%s)" % (self.display_name, self.name)

# set up mappers between your data tables and classes
mapper(Paste, paste_table,
    properties=dict(format=relation(Format, backref='pastes')))
mapper(Format, format_table)
mapper(Style, style_table)

# the identity schema

visits_table = Table('visit', metadata,
    Column('visit_key', String(40), primary_key=True),
    Column('created', DateTime, nullable=False, default=datetime.now),
    Column('expiry', DateTime)
)

visit_identity_table = Table('visit_identity', metadata,
    Column('visit_key', String(40), primary_key=True),
    Column('user_id', Integer, ForeignKey('tg_user.user_id'), index=True)
)

groups_table = Table('tg_group', metadata,
    Column('group_id', Integer, primary_key=True),
    Column('group_name', Unicode(16), unique=True),
    Column('display_name', Unicode(255)),
    Column('created', DateTime, default=datetime.now)
)

users_table = Table('tg_user', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', Unicode(16), unique=True),
    Column('email_address', Unicode(255), unique=True),
    Column('display_name', Unicode(255)),
    Column('password', Unicode(40)),
    Column('created', DateTime, default=datetime.now)
)

permissions_table = Table('permission', metadata,
    Column('permission_id', Integer, primary_key=True),
    Column('permission_name', Unicode(16), unique=True),
    Column('description', Unicode(255))
)

user_group_table = Table('user_group', metadata,
    Column('user_id', Integer, ForeignKey('tg_user.user_id',
        onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
    Column('group_id', Integer, ForeignKey('tg_group.group_id',
        onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
)

group_permission_table = Table('group_permission', metadata,
    Column('group_id', Integer, ForeignKey('tg_group.group_id',
        onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permission.permission_id',
        onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
)


# the identity model

class Visit(object):
    """A visit to your site."""

    @classmethod
    def lookup_visit(cls, visit_key):
        """Look up Visit by given visit key."""
        return cls.query.get(visit_key)


class VisitIdentity(object):
    """A Visit that is linked to a User object."""

    @classmethod
    def by_visit_key(cls, visit_key):
        """Look up VisitIdentity by given visit key."""
        return cls.query.get(visit_key)


class Group(object):
    """An ultra-simple group definition."""

    @classmethod
    def by_group_name(cls, group_name):
        """Look up Group by given group name."""
        return cls.query.filter_by(group_name=group_name).first()
    by_name = by_group_name


class User(object):
    """Reasonably basic User definition.

    Probably would want additional attributes.

    """
    @property
    def permissions(self):
        """Return all permissions os all groups the user belongs to."""
        p = set()
        for g in self.groups:
            p |= set(g.permissions)
        return p

    @classmethod
    def by_email_address(cls, email_address):
        """Look up User by given email address.

        This class method that can be used to search users based on their email
        addresses since it is unique.

        """
        return cls.query.filter_by(email_address=email_address).first()

    @classmethod
    def by_user_name(cls, user_name):
        """Look up User by given user name.

        This class method that permits to search users based on their
        user_name attribute.

        """
        return cls.query.filter_by(user_name=user_name).first()
    by_name = by_user_name

    def _set_password(self, password):
        """Run cleartext password through the hash algorithm before saving."""
        self._password = identity.encrypt_password(password)

    def _get_password(self):
        """Returns password."""
        return self._password

    password = property(_get_password, _set_password)


class Permission(object):
    """A relationship that determines what each Group can do."""

    @classmethod
    def by_permission_name(cls, permission_name):
        """Look up Permission by given permission name."""
        return cls.query.filter_by(permission_name=permission_name).first()
    by_name = by_permission_name


# set up mappers between identity tables and classes

mapper(Visit, visits_table)

mapper(VisitIdentity, visit_identity_table,
        properties=dict(users=relation(User, backref='visit_identity')))

mapper(User, users_table,
        properties=dict(_password=users_table.c.password))

mapper(Group, groups_table,
        properties=dict(users=relation(User,
                secondary=user_group_table, backref='groups')))

mapper(Permission, permissions_table,
        properties=dict(groups=relation(Group,
                secondary=group_permission_table, backref='permissions')))
