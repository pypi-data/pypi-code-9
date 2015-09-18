from pysplice._splice import ffi, lib
import os
import errno

from collections import namedtuple
Pipe = namedtuple('Pipe', 'fileno')

def mkpipe():
    readfd, writefd = os.pipe()
    return Pipe(lambda: readfd), Pipe(lambda: writefd)

def splice(infile, off_in, outfile, off_out, size, flags=0):
    off_in = ffi.NULL if off_in is None else ffi.new('loff_t *', off_in)
    off_out = ffi.NULL if off_out is None else ffi.new('loff_t *', off_out)
    while True:
        res = lib.splice(infile.fileno(), off_in,
                         outfile.fileno(), off_out,
                         size, flags)
        if res != -1:
            return res
        elif ffi.errno != errno.EINTR:
            raise OSError(ffi.errno, os.strerror(ffi.errno))
