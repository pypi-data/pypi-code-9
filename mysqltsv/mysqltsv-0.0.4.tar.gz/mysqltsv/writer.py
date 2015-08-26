import logging

from .util import write_row

logger = logging.getLogger("mysqltsv.reader")


class Writer:

    def __init__(self, f, headers=None, none_string="NULL"):
        self.f = f
        self.none_string = none_string

        if headers != None:
            write_row(headers, self.f, none_string=self.none_string)

        self.headers = headers

    def write(self, row):
        write_row(row, self.f, headers=self.headers,
                  none_string=self.none_string)
