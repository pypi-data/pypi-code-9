# -*- encoding: utf-8 -*-
from any2 import Any2Base
from openpyxl import Workbook


class List2xl(Any2Base):

    def __init__(self, target_filename, colnames=None):
        """Create an XLS writer that writes a list like iterator to an XLS file

        :param target_filename: the filename to serialize data to
        :return: Nothing

        :param colnames: a list of column names to use as the first line of you
        Excel file. If you provide a list of column names you'll be able to use
        a NameTransformer instead of a TypeTransformer, which permits to target
        more precisely the transformations you apply to which column.
        :type colnames: list of strings
        """
        # just pass no column mapping -> []
        super(List2xl, self).__init__(target_filename, [])
        self.wb = Workbook(optimized_write=True)
        self.colnames = colnames
        self.ws = self.wb.create_sheet()

    def prepend(self, row):
        """Prepend some data before writing from the data iterator
        :param row: a list or items read for writing to XLS. Used internally to
        set the column names as the first line
        :return: nothing
        """
        self.ws.append(row)

    def write(self, data_generator, write_names=False):
        """call this method when ready to input data in the file.
        Don't forget to call the finalize() method once your are finished
        adding data to the XLS file.

        :param data_generator: an iterable get data from and write to the XLS
        file. This must contain list like objects (ie: iterable objects)
        :param write_names: If this flag is set to True and you added column
        names to the constructor of this class then the first line of your file
        will contain the column names you passed then.
        :return: Nothing
        """

        if write_names and self.colnames:
            self.prepend(self.colnames)

        ws = self.ws

        for row in data_generator:
            ws.append(row)

    def finalize(self):
        """Actually write to the output file and save it to disk."""

        self.wb.save(self.target_filename)
