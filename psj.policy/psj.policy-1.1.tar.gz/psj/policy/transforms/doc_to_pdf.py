##
## doc_to_pdf.py
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
"""Convert MS words doc documents to PDF using OOo.
"""
from Products.PortalTransforms.interfaces import ITransform
from zope.interface import implements
from psj.policy.transforms import OOOTransformBase
from psj.policy.transforms.cmd_oooconv import Document


class Doc2Pdf(OOOTransformBase):
    """A transformation from MS word docs to PDF.

    Supports .doc and .docx.
    """
    implements(ITransform)

    inputs = (
        'application/msword',
        'application/vnd.openxmlformats-officedocument' +
        '.wordprocessingml.document',)
    output = 'application/pdf'
    output_encoding = 'utf-8'

    def name(self, name=None):
        """Return the name of the transform instance

        The second parameter is only here to satisfy the interface
        requirements, which seem to be broken.
        """
        return 'doc_to_pdf'

    def convert(self, data, idatastream, filename=None, mimetype=None,
                **kwargs):
        """Convert the data, store the result in idata and return that.
        """
        cache_dir = self.cache_dir or None
        cache_key = self.get_cache_key('cache_key_pdf', idatastream)
        extension = '.doc'
        if mimetype is not None:
            if mimetype == self.inputs[1]:
                extension = '.docx'
        filename = filename or 'unknown' + extension
        if not (filename.lower().endswith('.doc') or
                filename.lower().endswith('.docx')):
            filename += extension
        document = Document(filename, data, cache_dir=cache_dir)
        pdf, cache_key = document.convertToPDF(cache_key=cache_key)
        idatastream.getMetadata()['cache_key_pdf'] = cache_key
        idatastream.setData(pdf)
        return idatastream


def register():
    return Doc2Pdf()
