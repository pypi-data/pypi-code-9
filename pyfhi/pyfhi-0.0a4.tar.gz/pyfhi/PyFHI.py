#!/usr/bin/env python

"""Contains importable Open class to extend Python file handling"""

import sys

__version__ = '0.0a3'


class Open(object):
    """File-wrapping class with added functionality

    The Open correctly mimics all methods and attributes of Python File
    Objects. See Python documentation for information on said methods and
    attributes. Only improvements to File Objects will be documented here.

    This Class is meant to be functional in both Python 2.7+ and Python 3.4+.
    The next method in Python 2.7+ is next and __next__ in Python3.4+. The
    latter is awkward to write and requires users to change their script
    to obtain cross compatibility. In Open, both methods are available
    and both methods call the proper file method for the runtime Python
    version. As such, developers using Open due not need to alter file
    handling code to port between Python versions.

    Open tracks all file handles opened with Open. Calling the static method
    Open.close_all() will close all said file handles.

    Printing an instance of Open yields a summary of the instance as follows:
    File Name
    File Mode
    File Encoding
    File Closed
    """

    # Contains pointer for each instance of Open
    _open_instances = []

    def __init__(self, file, *args, **kwargs):
        """Initializes instance, opens file, and gets file attributes

        :rtype : None
        :param file: File to be opened
        :param args: Arguments to be passed to the File Object such as mode
        :param kwargs: Keyword Arguments version of args
        """

        # Initialize and record instance and open file
        self.file_handle = open(file, *args, **kwargs)
        self._open_instances.append(self)

        # Store File Object Attributes as Instance Attributes
        self.closed = self.file_handle.closed
        self.encoding = self.file_handle.encoding
        self.mode = self.file_handle.mode
        self.name = self.file_handle.name
        self.newlines = self.file_handle.newlines
        try:
            self.softspace = self.file_handle.softspace
        except AttributeError:
            self.softspace = 0

    def __str__(self):
        """Returns summary of Open instance self

        :rtype : str
        """

        message = 'File Name: {0}\nFile Mode: {1}\nFile Encoding: {2}\n' \
                  'File Closed: {3}\n'.format(self.name,
                                              self.mode,
                                              self.encoding,
                                              self.closed)
        return message

    def __enter__(self):
        """Makes Open compatible with 'with' statements

        :rtype : self
        """

        return self

    def __iter__(self):
        """Makes Open iterable

        :rtype : self
        """

        return self

    def __next__(self, *args, **kwargs):
        """Detects Python version, calls proper next method, and returns line

        :rtype : str
        :param args: Arguments to be passed the File Object
        :param kwargs: Keyword Arguments version of args
        """

        python_version = sys.version_info[0]
        if python_version == 3:
            return self.file_handle.__next__(*args, **kwargs)
        elif python_version == 2:
            return self.file_handle.next()

    def __exit__(self, exception_type, exception_value, traceback):
        """Called when a 'with' statement exits, closes file handle

        :rtype : None
        :param exception_type: Type of exception, if any
        :param exception_value: Value of exception, if any
        :param traceback: Traceback to error line, if any
        """

        self.close()

    @staticmethod
    def close_all():
        """Close all file handles opened with Open

        :rtype : None
        """

        file_handles = [copy for copy in Open._open_instances]
        for file_handle in file_handles:
            file_handle.close()

    # All following methods are essentially just file method wrappers.
    # It should be noted that each method could be created via adding
    # self.[method] = self.file_handle.[method] for each method to __init__.
    # I prefer to create a "new method" instead for the following reasons:
    #
    # 1. It is more clear what is a method and what is an attribute
    # 2. Each method essentially becomes a wrapper for the corresponding
    #    File Object wrapper.  This simplifies future editing of File Object
    #    methods within Open.
    # 3. It is easier for subclasses of Open to extend File Object methods.
    # 4. Provide custom documentation in addition to File Object documentation
    #    available online.

    def close(self):
        """Close file handle and modify appropriate instance variables

        :rtype : None
        """

        # The try...except block allows users to call close() multiple
        # times without an error.  This is consistent with File Objects.
        try:
            self._open_instances.remove(self)
            self.file_handle.close()
            self.closed = self.file_handle.closed
        except ValueError:
            pass

    def flush(self):
        """Flush internal buffer

        :rtype : None
        """

        self.file_handle.flush()

    def fileno(self):
        """Returns integer file descriptor

        :rtype : int
        """

        return self.file_handle.fileno()

    def isatty(self):
        """Returns True if file is connected to tty(-like) device

        :rtype : bool
        """

        return self.file_handle.isatty()

    def next(self, *args, **kwargs):
        """Detects Python version, calls proper next method, and returns line

        :rtype : str
        :param args: Arguments to be passed the File Object
        :param kwargs: Keyword Arguments version of args
        """

        return self.__next__(*args, **kwargs)

    def read(self, size=-1):
        """Returns rest of file or [size] bytes as a single string

        :rtype : str
        :param size: Max bytes to read from file
        """

        return self.file_handle.read(size)

    def readline(self, limit=-1):
        """Returns one line from the file unless [limit] bytes reached

        :rtype : str
        :param limit: Max bytes to read from file
        """

        return self.file_handle.readline(limit)

    def readlines(self, limit=-1):
        """Returns rest of file or [size] bytes as a list of lines

        :rtype : list
        :param limit: Max bytes to read from file
        """

        return self.file_handle.readlines(limit)

    def seek(self, offset, whence=0):
        """Set files position to [whence] + [offset] bytes

        :rtype : None
        :param offset: Number of bytes to move from whence [reference]
        :param whence: Reference position for [offset], possible values are:
                       0 = beginning of file [Default]
                       1 = current position
                       2 = end of file
        """
        self.file_handle.seek(offset, whence)

    def tell(self):
        """Return position in file in bytes

        :rtype : int
        """

        return self.file_handle.tell()

    def truncate(self, size=None):
        """Truncate file size to current position or [size]

        :rtype : None
        :param size: Number of bytes to truncate file to
        """

        if size is None:
            size = self.tell()
        self.file_handle.truncate(size)

    def write(self, string):
        """Write string to file

        :rtype : None
        :param string: String to write to file
        """

        self.file_handle.write(string)

    def writelines(self, sequence):
        """Write list of lines to file

        :rtype : None
        :param sequence: Any iterable containing line to write to file
        """

        self.file_handle.writelines(sequence)
