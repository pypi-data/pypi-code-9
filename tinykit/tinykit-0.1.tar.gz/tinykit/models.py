from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import jsonmodels.models
from six import add_metaclass


class TablenameMeta(type):
    """Adds ``__tablename__`` attribute to a class.
    """

    def __new__(cls, name, parents, attrs):
        # sets __tablename__ attribute in class;
        # default to class' lowercased name
        attrs.setdefault("__tablename__", name.lower())
        return type.__new__(cls, name, parents, attrs)


@add_metaclass(TablenameMeta)
class Model(jsonmodels.models.Base):
    """A base class for declared model class.

    This class should not be instantiated directly.
    """

    def __repr__(self):
        return "<{}: __tablename__={}>".format(
            self.__class__.__name__,
            self.__tablename__,
        )
