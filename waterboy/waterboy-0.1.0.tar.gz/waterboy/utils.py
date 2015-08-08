import os
import sys

try:
    import cPickle as _pickle
except ImportError:
    import pickle as _pickle

if sys.version_info[0] == 2:
    bytes = str

pathjoin = os.path.join
pathexists = os.path.exists
expanduser = os.path.expanduser
abspath = os.path.abspath
dirname = os.path.dirname

def pickle(value):
    return _pickle.dumps(value, protocol=_pickle.HIGHEST_PROTOCOL)

def unpickle(encoded_value):
    return _pickle.loads(bytes(encoded_value))

def import_module(path):
    __import__(path)
    return sys.modules[path]

def import_object(name):
    """Imports an object by name.

    import_object('x.y.z') is equivalent to 'from x.y import z'.

    """
    parts = name.split('.')
    m = '.'.join(parts[:-1])
    attr = parts[-1]
    obj = __import__(m, None, None, [attr], 0)
    try:
        return getattr(obj, attr)
    except AttributeError as e:
        raise ImportError("'%s' does not exist in module '%s'" % (attr, m))

