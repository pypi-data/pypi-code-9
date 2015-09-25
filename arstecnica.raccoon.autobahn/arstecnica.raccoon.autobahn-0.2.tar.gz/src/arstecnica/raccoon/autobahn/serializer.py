# -*- coding: utf-8 -*-
# :Progetto:  arstecnica.raccoon.autobahn -- JSON serializer replacement for Autobahn
# :Creato:    mar 07 lug 2015 22:29:34 CEST
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

"""
Custom JSON serializer
======================
"""

import decimal, uuid
import six

import nssjson

from autobahn.wamp.interfaces import IObjectSerializer, ISerializer
from autobahn.wamp.serializer import Serializer


dumps = nssjson.JSONEncoder(separators=(',', ':'),
                            use_decimal=True,
                            iso_datetime=True,
                            handle_uuid=True).encode
"Specialized JSON encoder function that knows about datetimes, decimals and UUID values."


loads = nssjson.JSONDecoder(parse_float=decimal.Decimal,
                            iso_datetime=True,
                            handle_uuid=True).decode
"Specialized JSON decoder function that knows about datetimes, decimals and UUID values."


class NssJsonObjectSerializer(object):
    """Implement JSON serialization thru `nssjson`__.

    Use ``nssjson`` capabilities to implement transparent
    serialization and deserialization of Python's ``date``,
    ``datetime``, ``Decimal`` and ``UUID`` instances.

    __ https://pypi.python.org/pypi/nssjson

    ::

      >>> import datetime, decimal, uuid
      >>> id = uuid.uuid3(uuid.NAMESPACE_OID, "example")
      >>> pi = decimal.Decimal("3.14159")
      >>> bd = datetime.date(1968, 3, 18)
      >>> print(dumps(id))
      "16eda250-39c7-3c5d-b2f8-7eb6dfedff40"
      >>> print(dumps(bd))
      "1968-03-18"
      >>> print(dumps(pi))
      3.14159

    ::

      >>> d = [id, bd, pi]
      >>> loads('["16eda250-39c7-3c5d-b2f8-7eb6dfedff40","1968-03-18",3.14159]') == d
      True
    """

    JSON_MODULE = nssjson
    BINARY = False

    def __init__(self, batched=False):
        """
        Ctor.

        :param batched: Flag that controls whether serializer operates in batched mode.
        :type batched: bool
        """
        self._batched = batched

    def serialize(self, obj):
        """
        Implements :func:`autobahn.wamp.interfaces.IObjectSerializer.serialize`
        """
        s = dumps(obj)
        if isinstance(s, six.text_type):
            s = s.encode('utf8')
        if self._batched:
            return s + b'\30'
        else:
            return s

    def unserialize(self, payload):
        """
        Implements :func:`autobahn.wamp.interfaces.IObjectSerializer.unserialize`
        """
        if self._batched:
            chunks = payload.split(b'\30')[:-1]
        else:
            chunks = [payload]
        if len(chunks) == 0:
            raise Exception("batch format error")
        return [loads(data.decode('utf8')) for data in chunks]


IObjectSerializer.register(NssJsonObjectSerializer)


class NssJsonSerializer(Serializer):
    "Custom JSON serializer for Autobahn."

    SERIALIZER_ID = "json"
    RAWSOCKET_SERIALIZER_ID = 1
    MIME_TYPE = "application/json"

    def __init__(self, batched=False):
        """
        Ctor.

        :param batched: Flag to control whether to put this serialized into batched mode.
        :type batched: bool
        """
        Serializer.__init__(self, NssJsonObjectSerializer(batched=batched))
        if batched:
            self.SERIALIZER_ID = "json.batched"


ISerializer.register(NssJsonSerializer)


def main():
    from datetime import date
    s = dumps([date.today(), uuid.uuid1(), "foo", decimal.Decimal('3.1415926')])
    print(s)
    print(loads(s))

if __name__ == '__main__':
    main()
