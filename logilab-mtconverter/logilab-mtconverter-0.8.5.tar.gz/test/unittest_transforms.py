# -*- coding: iso-8859-1 -*-
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

from logilab.mtconverter.engine import TransformEngine
from logilab.mtconverter import TransformData, TransformError, \
     register_base_transforms, register_pil_transforms

ENGINE = TransformEngine()
register_base_transforms(ENGINE)
register_pil_transforms(ENGINE)

import logilab.mtconverter as mtc
import os
import os.path as osp
import errno
import subprocess
DATAPATH = osp.dirname(__file__)

class MiscTransformsTC(TestCase):
    def test_html_to_text(self):
        data = TransformData(u'<b>yo (zou éà ;)</b>', 'text/html', 'utf8')
        converted = ENGINE.convert(data, 'text/plain').decode().strip()
        self.assertEqual(converted, u'**yo (zou éà ;)**')

        data = TransformData(u'<p>yo <br/>zogzog </p>', 'text/html', 'utf8')
        converted = ENGINE.convert(data, 'text/plain').decode().strip()
        self.assertEqual(converted, u'yo\n\nzogzog')

    def test_html_to_text_noenc(self):
        self.skipTest('Encoding detection with chardet does not work')
        # will trigger guess_encoding, check non-utf8 encoding
        data = TransformData(u"<b>yo (l'état à l'oeuf)</b>".encode('latin1'), 'text/html')
        self.assertIn(data.encoding, ('latin1', 'windows-1252'))
        data.check_encoding()

        converted = ENGINE.convert(data, 'text/plain').decode().strip()
        self.assertEqual(converted, u'**yo (zou éà ;)**')

    def test_xml_to_text(self):
        data = TransformData(u'<root><b>yo (zou éà ;)</b>a<tag/>b<root>', 'application/xml', 'utf8')
        converted = ENGINE.convert(data, 'text/plain').decode().strip()
        self.assertEqual(converted, u'yo (zou éà ;) a b')


    def test_pgpsignature_to_text(self):
        _data = u"""-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.9 (GNU/Linux)

iEYEARECAAYFAkxX5p8ACgkQkjcInxztrI64QQCggKA+PmbLYnGNtBB3Lb3pO3P8
r2MAoIO1DSsuM23SzgmqubGJEZuSRWhR
=GDDk
-----END PGP SIGNATURE-----
"""
        data = TransformData(_data, 'application/pgp-signature')
        converted = ENGINE.convert(data, 'text/plain').decode()
        self.assertMultiLineEqual(converted, _data)


    def test_odt_to_text(self):
        data = TransformData(open(osp.join(DATAPATH, 'hello.odt')),
                             'application/vnd.oasis.opendocument.text', 'utf8')
        converted = ENGINE.convert(data, 'text/plain').decode().strip()
        self.assertEqual(converted, u'Hello ! OpenOffice.org/2.4$Unix OpenOffice.org_project/680m17$Build-9310 Hello quoi de neuf doc ? bonjour 2008-07-08T16:19:35 2009-01-09T14:44:54 mot-clef 1 PT37S')
        # ZipFile will complain that
        # TypeError: file() argument 1 must be (encoded string without NULL bytes), not str
        # if given a plain str ... we shielded us from that.
        data = TransformData(open(osp.join(DATAPATH, 'hello.odt')).read(),
                             'application/vnd.oasis.opendocument.text', 'utf8')
        converted = ENGINE.convert(data, 'text/plain').decode().strip()
        self.assertEqual(converted, u'Hello ! OpenOffice.org/2.4$Unix OpenOffice.org_project/680m17$Build-9310 Hello quoi de neuf doc ? bonjour 2008-07-08T16:19:35 2009-01-09T14:44:54 mot-clef 1 PT37S')

    def test_pdf_to_text(self):
        try:
            subprocess.check_call(['pdflatex', 'hello'],
                                  cwd=osp.abspath(DATAPATH),
                                  stdout=open(os.devnull, 'w'))
        except OSError as exc:
            if exc.errno == errno.ENOENT:
                self.skipTest('pdflatex not installed')
            else:
                raise
        data = TransformData(open(osp.join(DATAPATH, 'hello.pdf')).read(),
                             'application/pdf', 'utf8')
        converted = ENGINE.convert(data, 'text/plain').decode().strip()
        self.assertEqual(converted, u'hello')

    def tearDown(self):
        for ext in ('pdf', 'aux', 'log'):
            try:
                os.unlink(osp.join(DATAPATH, 'hello.' + ext))
            except OSError:
                pass

if __name__ == '__main__':
    unittest_main()


