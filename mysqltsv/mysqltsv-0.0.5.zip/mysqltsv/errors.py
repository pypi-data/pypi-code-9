"""
.. autoclass:: mysqltsv.errors.RowReadingError
    :members:
"""


class RowReadingError(RuntimeError):
    """
    Thrown when an error occurs during TSV row reading.
    """
    def __init__(self, lineno, line, e):
        super().__init__("An error occurred while processing line #{0}:\n\t{1}"
                         .format(lineno, repr(line[:1000])))
        self.lineno = lineno
        """
        `int` : The line number that errored.
        """

        self.line = line
        """
        `str` : The line itself.
        """

        self.e = e
        """
        :class:`Exception` : The exception that was thrown.
        """
