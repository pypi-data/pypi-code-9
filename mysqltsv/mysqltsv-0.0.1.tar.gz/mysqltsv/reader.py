import logging

from .row_type import generate_row_type
from .util import read_row

logger = logging.getLogger("mysqltsv.reader")

class RowReadingError(RuntimeError):
    def __init__(self, lineno, line, e):
        super().__init__("An error occurred while processing line #{0}:\n\t{1}"
                         .format(lineno, repr(line[:1000])))
        self.lineno = lineno
        self.line = line
        self.e = e

def raise_exception(lineno, line, e):
    raise RowReadingError(lineno, line, e)


class Reader:

    def __init__(self, f, headers=True, types=None,
                          error_handler=raise_exception):
        self.f = f

        if headers == True:
            headers = list(read_row(f.readline()))
        elif hasattr(headers, "__iter__"):
            headers = list(headers)
        else:
            headers = None

        self.row_type = generate_row_type(headers, types)

        self.headers = headers
        self.error_handler = error_handler

    def __iter__(self):
        for i, line in enumerate(self.f):
            try:
                yield self.row_type(line)
            except Exception as e:
                lineno = i+1 if self.headers is None else i+2
                self.error_handler(lineno, line, e)

    def next(self):
        line = self.f.readline()
        if line != "":
            return self.row_type(line)
        else:
            raise StopIteration()
