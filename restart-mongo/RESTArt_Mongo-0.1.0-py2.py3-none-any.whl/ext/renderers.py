from __future__ import absolute_import

import csv
import codecs
from cStringIO import StringIO

from restart.renderers import Renderer


class UnicodeCSVWriter(object):
    """A CSV writer that can write Unicode rows to the CSV file,
    which is encoded in the given encoding.

    According to https://docs.python.org/2/library/csv.html::
        The standard version of the `csv` module does not
        support Unicode input.

    Borrowed from https://docs.python.org/2/library/csv.html#examples.
    """
    def __init__(self, csvfile, dialect=csv.excel,
                 encoding='utf-8', **kwargs):
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwargs)
        self.stream = csvfile
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([unicode(s).encode('utf-8') for s in row])

        # Fetch utf-8 output from the queue
        data = self.queue.getvalue()
        data = data.decode('utf-8')
        # And reencode it into the target encoding
        data = self.encoder.encode(data)

        # Write to the target stream
        self.stream.write(data)

        # Empty the queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.write(row)


class CSVRenderer(Renderer):
    """The CSV renderer class."""

    #: A tuple that specifies the columns in the CSV.
    #: Each item of `columns` is also a tuple in the form
    #: `(header, fieldname, converter)`.
    #:
    #: For example:
    #:
    #:     def capitalize(value):
    #:         return value.capitalize()
    #:
    #:     columns = (
    #:         # A simple fieldname with a customized `capitalize` converter
    #:         ('name', 'username', capitalize),
    #:         # A simple fieldname without converter
    #:         ('age', 'age', None),
    #:         # A nested fieldname with the built-in `unicode` converter
    #:         ('phone', 'contact.phone', unicode),
    #:         ...
    #:     )
    columns = None

    #: The default value for the missing field specified in the `columns`
    default_value = ''

    #: The content type bound to this renderer.
    content_type = 'text/csv'

    #: The format suffix bound to this renderer.
    format_suffix = 'csv'

    def render(self, data):
        """Render `data` into CSV.

        :param data: the data to be rendered.
        """
        assert isinstance(self.columns, tuple), \
            'The `columns` attribute must be a tuple object'
        assert isinstance(data, (dict, list, tuple)), \
            'The `data` argument must be a dict or a list or a tuple'

        # Assure that data is a sequence
        if isinstance(data, dict):
            data = [data]

        csv_file = StringIO()
        csv_writer = UnicodeCSVWriter(csv_file)

        # Write headers
        headers = [column[0] for column in self.columns]
        csv_writer.writerow(headers)

        # Write rows
        for each in data:
            values = []

            # Extract values
            for _, fieldname, converter in self.columns:
                keys = fieldname.split('.')

                # Get the value of `fieldname` from `each`
                value = each
                for key in keys:
                    value = value.get(key)
                    if value is None:
                        value = self.default_value
                        break

                # Convert the value if possible
                if converter is not None:
                    value = converter(value)

                values.append(value)

            # Write values
            csv_writer.writerow(values)

        csv_data = csv_file.getvalue()
        return csv_data
