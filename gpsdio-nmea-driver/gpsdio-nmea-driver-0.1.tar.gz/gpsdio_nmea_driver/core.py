"""
gpsdio NMEA driver
"""


import codecs

import ais.compatibility.gpsd
import ais.stream
from gpsdio.base import BaseDriver
import six


def parse_ais_stream(msg_stream):

    """
    Parse a stream of NMEA sentences, convert to GPSd, and yield.
    Parameters
    ----------
    msg_stream : iter
        An iterable producing one NMEA sentence per iteration.
    Yields
    ------
    dict
    """

    args = {
        'ignore_tagblock_station': True,
        'allow_unknown': True,
        'allow_missing_timestamps': True
    }

    gpsd_mangle = ais.compatibility.gpsd.Mangler(copy_tagblock_timestamp=True)
    for msg in map(gpsd_mangle, ais.stream.decode(msg_stream, **args)):
        yield msg


class _NMEAParser(object):

    """
    File-like object for interacting with the parser.
    """

    def __init__(self, f):
        if isinstance(f, six.string_types):
            self._f = codecs.open(f, encoding='utf-8')
        else:
            self._f = f
        self._parser = parse_ais_stream(self._f)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._parser)

    next = __next__

    def __getattr__(self, item):
        return getattr(self._f, item)


class NMEA(BaseDriver):

    io_modes = 'r',
    extensions = 'nmea',
    driver_name = 'NMEA'

    def open(self, name, mode='r'):
        return _NMEAParser(name)
