# -*- coding: utf-8 -*-
"""
    statico.readers
    ---------------
    Defines file parsers
    :license: MIT, see LICENSE for more details.
"""
import markdown


class Reader(object):
    def __init__(self, contents, reader_type):
        self.contents = contents
        self.reader_type = reader_type.lower()

    def read(self):
        if self.reader_type in ['md', 'markdown']:
            return markdown.markdown('\n'.join(self.contents), extensions=['markdown.extensions.extra',
                                                                           'markdown.extensions.codehilite'])

        if self.reader_type == 'html':
            return '\n'.join(self.contents)
