from __future__ import absolute_import, unicode_literals

import csv
import six
import xlrd
from functools import partial
from six.moves import cStringIO as StringIO

__all__ = ['read_csv_or_xls', 'utf8_reader']


def read_csv_or_xls(data):
    if isinstance(data, six.text_type):
        return data

    # Bytes.

    try:
        workbook = xlrd.open_workbook(file_contents=data)
    except xlrd.XLRDError:
        pass
    else:
        return read_workbook(workbook)

    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return None


def format_cell(workbook, cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        # Cannot use datetime here; it doesn't support years before 1900, and
        # often we get time-only values with the year 0.
        v = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*xlrd.xldate_as_tuple(cell.value, workbook.datemode))
    elif cell.ctype == xlrd.XL_CELL_NUMBER and int(cell.value) == cell.value:
        v = six.text_type(int(cell.value))
    else:
        v = six.text_type(cell.value)

    if six.PY2:
        v = v.encode('utf8')

    return v


def read_workbook(workbook):
    sio = StringIO()
    writer = csv.writer(sio)
    sh = workbook.sheet_by_index(0)
    for i in range(sh.nrows):
        writer.writerow(list(map(partial(format_cell, workbook), sh.row(i))))
    v = sio.getvalue()
    if not isinstance(v, six.text_type):
        v = v.decode('utf8')
    return v


def utf8_reader(data):
    if six.PY2:
        data = data.encode('utf8')
    csv_reader = csv.reader(data.splitlines(), skipinitialspace=True)
    for row in csv_reader:
        yield [cell.decode('utf8') if isinstance(cell, six.binary_type) else cell for cell in row]
