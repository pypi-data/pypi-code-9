"""
A set of convenience functions for processing
"""
import logging

from .reader import Reader
from .writer import Writer

logger = logging.getLogger("mysqltsv.functions")

def read(f, *args, **kwargs):
    """
    Reads a file and returns an iterator of
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
    return Reader(f, *args, **kwargs)

def write(rows, f, *args, **kwargs):
    """
    Writes an `iterable` of rows to to a file in TSV format.

    :Parameters:
        rows : `iterable`(`list` | `dict` | :class:`~mysqltsv.row_type.AbstractRow`)
            The rows to write.  
        f : `file`
            A file pointer to write rows to
        headers : `list`(`str`)
            If a list of `str` is provided, use those strings as headers.
            Otherwise, no headers are written.
        none_string : `str`
            A string that will be written as None when read.  (Defaults to
            "NULL")
    """
    writer = Writer(f, *args, **kwargs)

    for row in rows:
        writer.write(row)
