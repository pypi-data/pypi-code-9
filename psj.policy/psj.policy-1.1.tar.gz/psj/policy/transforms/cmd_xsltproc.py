##
## prog_xsltproc.py
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
Converters powered by the external xsltproc helper.
"""
import os
from os.path import isdir, dirname, join, abspath
from Products.PortalTransforms.libtransforms.commandtransform import (
    commandtransform,)
from Products.PortalTransforms.libtransforms.utils import sansext

XSL_STYLESHEET = abspath(join(dirname(__file__), 'document2xhtml.xsl'))


class Document(commandtransform):
    """A document that can be processed with xsltproc.
    """
    def __init__(self, name, data):
        """Initialize document.

        Append '.odt' to filename if missing and create a temporary
        directory for conversion.
        """
        if not name.lower().endswith('.odt'):
            name = name + '.odt'
        commandtransform.__init__(self, name, binary='xsltproc')
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
        """Convert the document to HTML.
        """
        if not os.name == 'posix':
            return
        name = self.name()
        cmd = 'cd "%s" && unzip "%s" 2>unzip_error.log 1>/dev/null' % (
            self.tmpdir, name)
        os.system(cmd)
        cmd = 'cd "%s" && %s --novalid "%s" content.xml '
        cmd += '> "%s.html" 2> "error.log"'
        cmd = cmd % (
            self.tmpdir, self.binary, XSL_STYLESHEET, sansext(name))
        os.system(cmd)
        try:
            htmlfile = open(os.path.join(
              self.tmpdir, "%s.html" % sansext(name)), 'r')
            html = htmlfile.read()
            htmlfile.close()
        except:
            try:
                return open(os.path.join(self.tmpdir, 'unzip_error.log'),
                            'r').read()
            except:
                return ''
        return html
