##
## doc_to_html.py
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
"""Convert MS words doc documents to XHTML using OOo and tidy.
"""
import os
from Products.PortalTransforms.interfaces import ITransform
from zope.interface import implements
from psj.policy.transforms import OOOTransformBase
from psj.policy.transforms.cmd_oooconv import Document


class Doc2Html(OOOTransformBase):
    """A transformation from MS word docs to HTML.
    """
    implements(ITransform)

    inputs = (
        'application/msword',
        'application/vnd.openxmlformats-officedocument' +
        '.wordprocessingml.document',
        )
    output = 'text/html'
    output_encoding = 'utf-8'

    def name(self, name=None):
        """Return the name of the transform instance

        The second parameter is only here to satisfy the interface
        requirements, which seem to be broken.
        """
        return 'doc_to_html'

    def convert(self, data, idatastream, filename='unknown', **kwargs):
        """Convert the data, store the result in idata and return that.
        """
        filename = filename or 'unknown.doc'
        cache_dir = self.cache_dir or None
        cache_key = self.get_cache_key('cache_key_html', idatastream)
        document = Document(filename, data, cache_dir=cache_dir)
        html, cache_key = document.convert(cache_key=cache_key)
        sub_objects_paths = [document.tmpdir,
                             os.path.join(document.tmpdir, 'Pictures')]
        objects = {}
        for path in sub_objects_paths:
            if os.path.exists(path):
                spath, images = document.subObjects(path)
                if images:
                    document.fixImages(spath, images, objects)
        idatastream.getMetadata()['cache_key_html'] = cache_key
        idatastream.setData(html)
        idatastream.setSubObjects(objects)
        return idatastream


def register():
    return Doc2Html()
