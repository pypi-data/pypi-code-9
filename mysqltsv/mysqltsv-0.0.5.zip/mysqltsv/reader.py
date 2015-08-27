"""
This module provides a set of utilities for reading TSV files.

.. autoclass:: mysqltsv.reader.Reader
    :members:

.. autofunction:: mysqltsv.functions.read

"""

import logging

from .errors import RowReadingError
from .row_type import generate_row_type
from .util import read_row

logger = logging.getLogger(__name__)


def raise_exception(lineno, line, e):
    raise RowReadingError(lineno, line, e)


class Reader:
    """
    Constructs a new TSV row reader -- which acts as an iterable of
    :class:`~mysqltsv.row_type.AbstractRow`.

    :Parameters:
        f : `file`
            A file pointer
        headers : `bool` | `list`(`str`)
            If True, read the first row of the file as a set of headers.  If a
            list of `str` is provided, use those strings as headers.  Otherwise,
            assume no headers.
        types : `list`( `callable` )
            A list of `callable` to apply to the row values.  If none is
            provided, all values will be read as `str`
        none_string : `str`
            A string that will be interpreted as None when read.  (Defaults to
            "NULL")
        error_handler : `callable`
            A function that takes three arguements (lineno, line, exception)
            that handles an error during row reading.  The default behavior is
            to throw a :class:`mysqltsv.errors.RowReadingError`
    """
    def __init__(self, f, headers=True, types=None, none_string="NULL",
                          error_handler=raise_exception):
        self.f = f

        if headers == True:
            headers = list(read_row(f.readline()))
        elif hasattr(headers, "__iter__"):
            headers = list(headers)
        else:
            headers = None

        self.row_type = generate_row_type(headers, types=types,
                                          none_string=none_string)

        self.headers = headers
        """
        `list`(`str`) : A list of headers if provided
        """

        self.none_string = none_string

        self.error_handler = error_handler

    def __iter__(self):
        for i, line in enumerate(self.f):
            try:
                yield self.row_type(line)
            except Exception as e:
                lineno = i+1 if self.headers is None else i+2
                self.error_handler(lineno, line, e)

    def __next__(self):
        line = self.f.readline()
        if line != "":
            return self.row_type(line)
        else:
            raise StopIteration()
