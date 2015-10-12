import sys
py3k = sys.version_info >= (3, 0)

if py3k:
    string_types = str,
    binary_type = bytes
    text_type = str
else:
    string_types = basestring,
    binary_type = str
    text_type = unicode


if py3k:
    from configparser import ConfigParser as SafeConfigParser
    import configparser
else:
    from ConfigParser import SafeConfigParser
    import ConfigParser as configparser


if py3k:
    from io import StringIO
else:
    # accepts strings
    from StringIO import StringIO

if py3k:
    import queue
else:
    import Queue as queue

if py3k:
    raw_input = input
else:
    raw_input = raw_input


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass.

    Drops the middle class upon creation.

    Source: http://lucumr.pocoo.org/2013/5/21/porting-to-python-3-redux/

    """

    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})
