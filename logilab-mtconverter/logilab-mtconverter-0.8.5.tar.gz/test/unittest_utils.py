# -*- coding: utf-8 -*-
# copyright 2006-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-mtconverter.
#
# logilab-mtconverter is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License, or (at your
# option) any later version.
#
# logilab-mtconverter is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-mtconverter. If not, see <http://www.gnu.org/licenses/>.
from logilab.common.testlib import TestCase, unittest_main

import locale
from StringIO import StringIO
from logilab.mtconverter import *

SPECIAL_CHARS = {
    '\f' : '\n',
    '\b' : ' ',
    '\n' : '\n',
    '\r' : '\r',
    '\r\n' : '\r\n',
    '\t' : '\t',
    '\v' : '\n',
    }

class HtmlEscapeTC(TestCase):

    def test_escape(self):
        for data, expected in [('toto', 'toto'),
                               ('r&d', 'r&amp;d'),
                               ('23<12 && 3>2', '23&lt;12 &amp;&amp; 3&gt;2'),
                               ('d"h"', 'd&quot;h&quot;'),
                               ("h'", 'h&#39;'),
                               ]:
            yield self.assertEqual, xml_escape(data), expected

    def test_escape_special_chars(self):
        for car, trcar in SPECIAL_CHARS.items():
            yield self.assertEqual, xml_escape(car), trcar
        for carnum in xrange(32):
            car = chr(carnum)
            if car in SPECIAL_CHARS:
                continue
            yield self.assertEqual, xml_escape(car), ' '
        yield self.assertEqual, xml_escape(u'é'), u'é'

    def test_escape_special_chars_unicode(self):
        for car, trcar in SPECIAL_CHARS.items():
            yield self.assertEqual, xml_escape(unicode(car)), trcar
        for carnum in xrange(32):
            car = chr(carnum)
            if car in SPECIAL_CHARS:
                continue
            yield self.assertEqual, xml_escape(unicode(car)), ' '

    def test_html_unescape(self):
        for data, expected in [('toto', 'toto'),
                               ('r&amp;d', 'r&d' ),
                               ('23&lt;12 &amp;&amp; 3&gt;2', '23<12 && 3>2'),
                               ('d&quot;h&quot;', 'd"h"'),
                               ('h&#39;', "h'"),
                               ('x &equiv; y', u"x \u2261 y"),
                               ]:
            yield self.assertEqual, html_unescape(data), expected


class GuessEncodingTC(TestCase):

    def test_emacs_style_declaration(self):
        data = '''# -*- coding: latin1 -*-'''
        self.assertEqual(guess_encoding(data), 'latin1')

    def test_emacs_style_declaration_stringIO(self):
        data = '''# -*- coding: latin1 -*-'''
        self.assertEqual(guess_encoding(StringIO(data)), 'latin1')

    def test_xml_style_declaration(self):
        data = '''<?xml version="1.0" encoding="latin1"?>
        <root/>'''
        self.assertEqual(guess_encoding(data), 'latin1')

    def test_html_style_declaration(self):
        data = '''<html xmlns="http://www.w3.org/1999/xhtml" xmlns:erudi="http://www.logilab.fr/" xml:lang="fr" lang="fr">
<head>
<base href="http://intranet.logilab.fr/jpl/" /><meta http-equiv="content-type" content="text/html; charset=latin1"/>
</head>
<body><p>hello world</p>
</body>
</html>'''
        self.assertEqual(guess_encoding(data), 'latin1')

    def test_bad_detection(self):
        data = '''class SchemaViewer(object):
    """return an ureport layout for some part of a schema"""
    def __init__(self, req=None, encoding=None):
'''
        # ascii detected by chardet
        try:
            import chardet
            self.assertEqual(guess_encoding(data), 'ascii')
        except ImportError:
            self.assertEqual(guess_encoding(data), DEFAULT_ENCODING)

class GuessMimetymeAndEncodingTC(TestCase):
    def test_base(self):
        format, encoding = guess_mimetype_and_encoding(filename=u"foo.txt", data="xxx")
        self.assertEqual(format, u'text/plain')
        self.assertEqual(encoding, locale.getpreferredencoding())

    def test_set_mime_and_encoding_gz_file(self):
        format, encoding = guess_mimetype_and_encoding(filename=u"foo.txt.gz", data="xxx")
        self.assertEqual(format, u'text/plain')
        self.assertEqual(encoding, u'gzip')
        format, encoding = guess_mimetype_and_encoding(filename=u"foo.txt.gz", data="xxx",
                                                       format='application/gzip')
        self.assertEqual(format, u'text/plain')
        self.assertEqual(encoding, u'gzip')
        format, encoding = guess_mimetype_and_encoding(filename=u"foo.gz", data="xxx")
        self.assertEqual(format, u'application/gzip')
        self.assertEqual(encoding, None)

    def test_set_mime_and_encoding_bz2_file(self):
        format, encoding = guess_mimetype_and_encoding(filename=u"foo.txt.bz2", data="xxx")
        self.assertEqual(format, u'text/plain')
        self.assertEqual(encoding, u'bzip2')
        format, encoding = guess_mimetype_and_encoding(filename=u"foo.txt.bz2", data="xxx",
                                                       format='application/bzip2')
        self.assertEqual(format, u'text/plain')
        self.assertEqual(encoding, u'bzip2')
        format, encoding = guess_mimetype_and_encoding(filename=u"foo.bz2", data="xxx")
        self.assertEqual(format, u'application/bzip2')
        self.assertEqual(encoding, None)

    def test_set_mime_and_encoding_unknwon_ext(self):
        format, encoding = guess_mimetype_and_encoding(filename=u"foo.789", data="xxx")
        self.assertEqual(format, u'application/octet-stream')
        self.assertEqual(encoding, None)


class TransformDataTC(TestCase):
    def test_autodetect_encoding_if_necessary(self):
        data = TransformData('''<?xml version="1.0" encoding="latin1"?>
        <root/>''', 'text/xml')
        self.assertEqual(data.encoding, 'latin1')


if __name__ == '__main__':
    unittest_main()
