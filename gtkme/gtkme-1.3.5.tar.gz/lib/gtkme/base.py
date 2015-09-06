# Detect Python3 and which OS for temperments.
import platform
PY3 = platform.python_version()[0] == '3'

if PY3:
    # pylint: disable=W0622
    unicode = str
    basestring = str

