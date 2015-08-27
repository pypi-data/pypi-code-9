"""
This module provides a set of utilities for writing TSV files.

.. autoclass:: mysqltsv.writer.Writer
    :members:

.. autofunction:: mysqltsv.functions.write

"""
import logging

from .util import write_row

logger = logging.getLogger(__name__)


class Writer:
    """
    Constructs a new TSV row writer.

    :Parameters:
        f : `file`
            A file pointer to write rows to
        headers : `list`(`str`)
            If a list of `str` is provided, use those strings as headers.
            Otherwise, no headers are written.
        none_string : `str`
            A string that will be written as None when read.  (Defaults to
            "NULL")
    """

    def __init__(self, f, headers=None, none_string="NULL"):
        self.f = f
        self.none_string = none_string

        if headers != None:
            write_row(headers, self.f, none_string=self.none_string)

        self.headers = headers

    def write(self, row):
        """
        Writes a row to the output file.

        :Parameters:
            row : `list` | `dict` | :class:`~mysqltsv.row_type.AbstractRow`
                Datastructure representing the row to write
        """
        write_row(row, self.f, headers=self.headers,
                  none_string=self.none_string)
