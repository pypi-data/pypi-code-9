##
## xslttrans.py
##
## Copyright (C) 2008, 2013 Uli Fouquet
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""
Converters doing xslt transforms.

This is suitable for XML based document formats like OOo or docx. It
requires the source files to be zipped and an XSLT stylesheet for the
actual transformation.

The output is determined by the XSL stylesheet and can be any
format. Most usual, however, are HTML and plain text.

The default XSL stylesheets and document paths used here apply to OOo
documents.

"""
import os
from os.path import isdir, dirname, join, abspath
from lxml import etree
from Products.PortalTransforms.libtransforms.commandtransform import (
    commandtransform,)

XSL_STYLESHEET = abspath(join(dirname(__file__), 'document2xhtml.xsl'))


def xslt_transform(stylesheet, xml_doc):
    """Transform a document using ans XSLT stylesheet.
    """
    xslt_doc = etree.parse(stylesheet)
    transform = etree.XSLT(xslt_doc)
    doc = etree.parse(xml_doc)
    return transform(doc)


class Document(commandtransform):
    """A document that can be unzipped and processed with lxml.
    """

    xsl_stylesheet_path = XSL_STYLESHEET
    xml_doc_path = 'content.xml'

    def __init__(self, name, data,
                 xsl_stylesheet_path=None,
                 xml_doc_path=None):
        """Initialize document.

        Store stylesheet and other important data, then create a
        temporary directory for conversion.
        """
        self.xsl_stylesheet = xsl_stylesheet_path or self.xsl_stylesheet_path
        self.xml_doc = xml_doc_path or self.xml_doc_path
        commandtransform.__init__(self, name)
        name = self.name()
        self.tmpdir, self.fullname = self.initialize_tmpdir(
            data, filename=name)

    def __del__(self):
        """Remove the temporary directory and loop on all base
        destructors.

        This method is protected against diamond inheritance.
        """
        if isdir(self.tmpdir):
            self.cleanDir(self.tmpdir)
        basekeys = []
        for base in self.__class__.__bases__:
            basekey = str(base)
            if basekey in basekeys:
                continue
            basekeys.append(basekey)
            if hasattr(base, '__del__'):
                base.__del__(self)

    def convert(self):
        """Convert the document according to the XSL stylesheet.
        """
        # Unzip the file...
        name = self.name()
        cmd = 'cd "%s" && unzip "%s" 2>unzip_error.log 1>/dev/null' % (
            self.tmpdir, name)
        os.system(cmd)

        # Do the transformation...
        stylesheet = open(self.xsl_stylesheet_path, 'r')
        xml_doc = open(os.path.join(self.tmpdir, self.xml_doc_path), 'r')
        result = str(xslt_transform(
            stylesheet, xml_doc))
        xml_doc.close()
        stylesheet.close()
        return result
