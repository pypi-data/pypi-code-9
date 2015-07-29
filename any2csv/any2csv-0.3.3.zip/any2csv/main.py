# -*- encoding: utf-8 -*-
import logging
import csv
from csv import DictWriter
import shutil
import codecs
from pyjon.utils import get_secure_filename
import six
from any2.exceptions import Any2Error
from any2.exceptions import ColumnMappingError
from any2 import DictAdapter as CSVAddon

log = logging.getLogger(__name__)


class Any2CSVError(Any2Error):
    pass


class Any2Dialect(csv.Dialect, object):

    def __init__(self, delimiter, quoting, quotechar, lineterminator):
        self.delimiter = delimiter
        self.quoting = quoting
        self.quotechar = quotechar
        self.lineterminator = lineterminator
        super(Any2Dialect, self).__init__()


class Any2CSV(object):

    def __init__(
            self, target_filename, column_mappings,
            encoding='UTF-8',
            delimiter=';',
            quoting=csv.QUOTE_ALL,
            quotechar='"',
            lineterminator='\n',
            show_first_line=False
    ):
        """Initialize the Any2CSV.

        :param target_filename: The target csv file name
        :type target_filename: String

        :param column_mappings: Mapping to use
        :type column_mappings: list of dictionary with keys :
            - attr
            - colname
            - renderer (callback function or string)

            The renderer callback must accept one argument the object,
            the result must be unicode type

        :param encoding: The encoding to use to write the final csv file
        :type encoding:String

        :param delimiter: The delimiter to use to separate each field on
        the final csv file, default delimiter is ";"
        :type delimiter: String

        :param quoting: The quoting policy for the CSV writer, default is
        csv.QUOTE_ALL
        :type quoting: one of csv.QUOTE_*

        :param quotechar: The character to be used as a quote, default='"'
        :type quotechar: string

        :param lineterminator: The line terminator to use in our CSV dialect
        :type lineterminator: binary string

        :param show_first_line: Show the csv header with all column names,
        default is False
        :type show_first_line: Boolean
        """
        self.encoding = encoding
        self.target_filename = target_filename
        self.column_mappings = column_mappings
        self.check_column_mappings()
        self.delimiter = delimiter
        self.show_first_line = show_first_line

        self.__tmp_filename = get_secure_filename()
        self.__tmp_file = codecs.open(
            self.__tmp_filename, 'wb+',
            encoding=self.encoding
        )

        csv.register_dialect(
            'any2csv_dialect',
            Any2Dialect(delimiter, quoting, quotechar, lineterminator),
        )

        self.csvengine = DictWriter(
            self.__tmp_file,
            self.__get_column_names(),
            dialect='any2csv_dialect'
        )

    def check_column_mappings(self):
        attr = None
        renderer = None
        colname = None

        for column_mapping in self.column_mappings:
            attr = column_mapping.get('attr', None)
            renderer = column_mapping.get('renderer', None)
            colname = column_mapping.get('colname', None)

        if colname is None:
            raise ColumnMappingError(
                'The colname is mandatory on the column mapping'
            )

        if renderer is not None:
            if not (
                isinstance(renderer, six.string_types) or callable(renderer)
            ):
                msg = "Renderer definition error from the column_mapping,"
                msg += " renderer must be only string/unicode or "
                msg += "callable, not %s" % type(renderer)

                raise ColumnMappingError(msg)

        if renderer is None and attr is None:
            msg = 'On the column mapping definition,'
            msg += ' you must define at least attr or renderer'
            raise ColumnMappingError(msg)

        if attr is None and callable(renderer):
            msg = 'You cannot use a callable renderer if attr is not defined.'
            raise ColumnMappingError(msg)

    def __get_column_attributes(self):
        return [col_def['attr'] for col_def in self.column_mappings]

    def __get_column_names(self):
        return [col_def['colname'] for col_def in self.column_mappings]

    def __write_firstrow(self):
        firstrow = dict()
        for colname in self.__get_column_names():
            firstrow[colname] = colname
        self.csvengine.writerow(firstrow)

    def write(self, data_generator):
        if self.show_first_line:
            self.__write_firstrow()

        for data in data_generator:
            adapted_data = CSVAddon(
                data,
                self.column_mappings,
                self.encoding
            )

            log.debug("writing row keys: %s, values: %s" % (
                adapted_data.keys(), adapted_data.obj.__dict__))
            self.csvengine.writerow(adapted_data)

        self.__tmp_file.close()
        self.__write_target_file(self.__tmp_filename)

    def __write_target_file(self, temp_filename):
        shutil.move(temp_filename, self.target_filename)
