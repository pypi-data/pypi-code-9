#-*-encoding:utf-8-*-
import contextlib
import sys

@contextlib.contextmanager
def sopen(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()
