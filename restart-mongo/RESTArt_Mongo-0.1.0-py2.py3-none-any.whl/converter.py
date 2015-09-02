from __future__ import absolute_import

from werkzeug.routing import BaseConverter


class ObjectIdConverter(BaseConverter):
    """This converter only accepts ObjectId strings::

        Rule('/object/<objectid:identifier>')
    """

    def to_python(self, value):
        pass

    def to_url(self, value):
        pass
