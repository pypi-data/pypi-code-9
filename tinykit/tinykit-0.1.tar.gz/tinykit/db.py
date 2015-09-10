from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import tinydb
import tinyrecord


class Database(object):
    """A class acts as a wrapper of ``tinydb.TinyDB`` with
    additional features.

    Typical usage::

        db = Database("/path/to/db.json")
        table = db.table("testing")

        with db.transaction(table) as tr:
            tr.insert({"label": "database"})

        table.get(db.where("label") == "database")

    When using a subclass of ``tinykit.models.Model``::

        from jsonmodels.fields import StringField


        class TestingModel(Model):
            __tablename__ = "testing"
            label = StringField()

        model = TestingModel()
        model.label = "database"

        db = Database("/path/to/db.json")
        table = db.table(model.__tablename__)

        with db.transaction(table) as tr:
            tr.insert(model.to_struct())

        table.get(db.where("label") == model.label)

    :param args: Positional arguments passed to the underlying
                 ``tinydb.TinyDB`` object.
    :param kwargs: Keyword arguments passed to the underlying
                   ``tinydb.TinyDB`` object.
    """

    def __init__(self, *args, **kwargs):
        # A reference to the actual database object.
        self._conn = tinydb.TinyDB(*args, **kwargs)

        # A shortcut to ``tinydb.TinyDB.table`` method.
        # See http://tinydb.readthedocs.org/en/latest/usage.html#tables
        # for reference.
        self.table = self._conn.table

        # A shortcut to ``tinydb.where`` object.
        # See http://tinydb.readthedocs.org/en/latest/usage.html#queries
        # for reference.
        self.where = tinydb.where

        # A shortcut to ``tinyrecord.transaction`` object.
        # See https://github.com/eugene-eeo/tinyrecord
        # for reference.
        self.transaction = tinyrecord.transaction

    def __repr__(self):
        return "<{}: storage={}>".format(
            self.__class__.__name__,
            self._conn._storage.__class__.__name__,
        )
