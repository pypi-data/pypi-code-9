from collections import namedtuple as _namedtuple

VERSION_INFO = _namedtuple('version_info', ('major', 'minor', 'patch'))(0, 1, 0)
VERSION = "%d.%d.%d" % VERSION_INFO
