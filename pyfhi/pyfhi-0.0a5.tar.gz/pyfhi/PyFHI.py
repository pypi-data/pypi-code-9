#!/usr/bin/env python

"""Contains Open and filecloser, the two key components of PyFHI

This file is essentially all there is to PyFHI (Python File Handling Improved),
one simply needs to import the one function and one class of this file to
receive the functionality improvements of PyFHI. The README contains details
of Open and filecloser but a minimally functional explanation of proper
usage follows:

import pyfhi
Change all instances of 'open' to 'Open' (capitalize the 'O', this doesn't
                                          apply to things such as os.open)
Add '@filecloser' before each function you wish to wrap (ideally main())
"""

import sys

__version__ = '1.0.0'


class Open(object):
    """File-wrapping class with added functionality and improved features

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

        :param file: File to be opened
        :type file: str

        :param args: Arguments to be passed to the File Object such as mode
        :type args: various

        :param kwargs: Keyword Arguments version of args
        :type kwargs: various
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

        :returns : instance-dependent data on the file handle
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

        :returns : self
        :rtype : class
        """

        return self

    def __iter__(self):
        """Makes Open iterable

        :returns : self
        :rtype : class
        """

        return self

    def __next__(self, *args, **kwargs):
        """Detects Python version, calls proper next method, and returns line

        :returns : Next line of file
        :rtype : str

        :param args: Arguments to be passed the File Object
        :type args: various

        :param kwargs: Keyword Arguments version of args
        :type kwargs: various
        """

        python_version = sys.version_info[0]
        if python_version == 3:
            return self.file_handle.__next__(*args, **kwargs)
        elif python_version == 2:
            return self.file_handle.next()

    def __exit__(self, exception_type, exception_value, traceback):
        """Called when a 'with' statement exits, closes file handle

        :param exception_type: Type of exception, if any
        :type exception_type: type

        :param exception_value: Value of exception, if any
        :type exception_value: error-dependent

        :param traceback: Traceback to error line, if any
        :type traceback: traceback
        """

        self.close()
        print(type(exception_type))
        print(type(exception_value))
        print(type(traceback))

    @staticmethod
    def close_all():
        """Close all file handles opened with Open"""

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
        """Close file handle and modify appropriate instance variables"""

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
        """

        self.file_handle.flush()

    def fileno(self):
        """Returns integer file descriptor

        :returns : File descriptor
        :rtype : int
        """

        return self.file_handle.fileno()

    def isatty(self):
        """Returns True if file is connected to tty(-like) device

        :returns : True if file connected to tty(-like) device, else False
        :rtype : bool
        """

        return self.file_handle.isatty()

    def next(self, *args, **kwargs):
        """Detects Python version, calls proper next method, and returns line

        :returns : Next line of file
        :rtype : str

        :param args: Arguments to be passed the File Object
        :type args: various

        :param kwargs: Keyword Arguments version of args
        :type kwargs: various
        """

        return self.__next__(*args, **kwargs)

    def read(self, limit=-1):
        """Returns rest of file or [limit] bytes as a single string

        :returns : Rest of file or [limit] bytes
        :rtype : str

        :param limit: Max bytes to read from file
        :type limit: int
        """

        return self.file_handle.read(limit)

    def readline(self, limit=-1):
        """Returns one line from the file unless [limit] bytes reached

        :returns : Next line of file or [limit] bytes
        :rtype : str

        :param limit: Max bytes to read from file
        :type limit:
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

        :param offset: Number of bytes to move from whence [reference]
        :type offset: int

        :param whence: Reference position for [offset], possible values are:
                       0 = beginning of file [Default]
                       1 = current position
                       2 = end of file
        :type whence: int
        """
        self.file_handle.seek(offset, whence)

    def tell(self):
        """Return position in file in bytes

        :returns : Position in file in bytes
        :rtype : int
        """

        return self.file_handle.tell()

    def truncate(self, size=None):
        """Truncate file size to current position or [size]

        :param size: Number of bytes to truncate file to
        :type size: int
        """

        if size is None:
            size = self.tell()
        self.file_handle.truncate(size)

    def write(self, string):
        """Write string to file

        :param string: String to write to file
        :type string: str
        """

        self.file_handle.write(string)

    def writelines(self, sequence):
        """Write list of lines to file

        :param sequence: Any iterable containing line to write to file
        :type sequence: iterable
        """

        self.file_handle.writelines(sequence)


def filecloser(function):
    """Calls the wrapper passing [function] and returns the wrapped function

    :returns: The function within a wrapper that closes all files after running
    :rtype : function

    :param function: The function to wrap
    :type function: function
    """

    def filecloser_wrapper(*args, **kwargs):
        """Wraps [function] in try...finally block to close all files

        :param args: Arguments to be passed to the File Object such as mode
        :type args: various

        :param kwargs: Keyword Arguments version of args
        :type kwargs: various
        """

        try:
            function(*args, **kwargs)
        finally:
            Open.close_all()
    return filecloser_wrapper
