# -*- coding: utf-8 -*-

__version__ = '0.1.3'
__author__ = 'Ossama Edbali (ossedb@gmail.com)'


import markdown


class Reader(object):
    def __init__(self, contents, reader_type):
        self.contents = contents
        self.reader_type = reader_type

    def read(self):
        if self.reader_type == 'md':
            return markdown.markdown('\n'.join(self.contents), extensions=['markdown.extensions.extra',
                                                                           'markdown.extensions.codehilite'])

        if self.reader_type == 'html':
            return '\n'.join(self.contents)
