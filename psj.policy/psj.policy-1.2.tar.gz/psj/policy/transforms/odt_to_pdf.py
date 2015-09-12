##
## odt_to_pdf.py
##
## Copyright (C) 2008, 2013, 2015 Uli Fouquet
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
from Products.PortalTransforms.interfaces import ITransform
from zope.interface import implements
from psj.policy.transforms import OOOTransformBase
from psj.policy.transforms.cmd_oooconv import Document


class Odt2Pdf(OOOTransformBase):
    """A transformation from OpenOffice docs to PDF/A.
    """
    implements(ITransform)

    inputs = ('application/vnd.oasis.opendocument.text',)
    output = 'application/pdf'

    def name(self, name=None):
        """Return the name of the transform instance

        The second parameter is only here to satisfy the interface
        requirements, which seem to be broken.
        """
        return 'odt_to_pdf'

    def convert(self, data, idatastream, filename=None, **kwargs):
        """Convert the data, store the result in idata and return that.
        """
        cache_dir = self.cache_dir or None
        cache_key = self.get_cache_key('cache_key_pdf', idatastream)
        filename = filename or 'unknown.odt'
        if not filename.lower().endswith('.odt'):
            filename += '.odt'
        document = Document(filename, data, cache_dir=cache_dir)
        pdf, cache_key = document.convertToPDF(cache_key=cache_key)
        idatastream.getMetadata()['cache_key_pdf'] = cache_key
        idatastream.setData(pdf)
        return idatastream


def register():
    return Odt2Pdf()
