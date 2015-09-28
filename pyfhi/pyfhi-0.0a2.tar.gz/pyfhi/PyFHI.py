#!/usr/bin/env python

"""


"""

__version__ = '0.0a1'

# TODO: Test this class heavily
class Open(object):

    _file_handles = []

    def __init__(self, file, *args, **kwargs):

        self.file_handle = open(file, *args, **kwargs)
        self._file_handles.append(self.file_handle)
        self.closed = self.file_handle.closed
        self.encoding = self.file_handle.encoding
        self.mode = self.file_handle.mode
        self.name = self.file_handle.name
        self.newlines = self.file_handle.newlines

        # This variable only exists for compatibility reasons.
        self.softspace = 0


    def __enter__(self):

        return self

    def __next__(self, *args, **kwargs):

        return self.file_handle.__next__(*args, **kwargs)

    def __exit__(self, exception_type, exception_value, traceback):

        self._file_handles.remove(self.file_handle)
        self.file_handle.close()

    def close(self):

        self._file_handles.remove(self.file_handle)
        self.file_handle.close()

    def flush(self, *args):

        self.file_handle.flush()

    def fileno(self):

        return self.file_handle.fileno()

    def isatty(self):

        return self.file_handle.isatty()

    def read(self, size=-1):

        return self.file_handle.read(size)

    def readline(self, limit=-1):

        return self.file_handle.readline(limit)

    def readlines(self, limit=-1):

        return self.file_handle.readline(limit)

    def seek(self, offset, whence=0):

        self.file_handle.seek(offset, whence)

    def tell(self):

        return self.file_handle.tell()

    def truncate(self, size=None):

        if size is None:
            size = self.tell()
        self.file_handle.truncate(size)

    def write(self, string):

        self.file_handle.write(string)

    def writelines(self, sequence):

        self.file_handle.writelines(sequence)
