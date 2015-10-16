# coding=utf-8
"""
This module provides compatibility with the Python 3
"""
import sys

# Get Python version
PY2 = sys.version_info[0] == 2

if PY2:  # Python 2 namespace
    text_type = unicode
    string_types = (str, unicode)
    unichr = unichr

    import types
    NoneType = types.NoneType
else:  # Python 3 namespace
    text_type = str
    string_types = (str,)
    unichr = chr
    NoneType = type(None)


# Some magic
def with_metaclass(meta, *bases):
    class MetaClass(meta):
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
        
    return MetaClass('temporary_class', None, {})
