##
## __init__.py
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
from Products.PortalTransforms.libtransforms.utils import MissingBinary


class OOOTransformBase(object):
    """A transformation base for OpenOffice.org-based transforms.

    This base supports configuration parameters shared by all local
    OO.o transforms.
    """
    def __init__(self, name=None, cache_dir=''):
        self.config = {'cache_dir': cache_dir}
        self.config_metadata = {
        'cache_dir': (
            'string', 'Cache Directory',
            'Directory for caching results. Leave empty for no cache.'),
        }
        if name:
            self.__name__ = name

    def __getattr__(self, name):
        if name in self.config:
            return self.config[name]
        raise AttributeError(name)

    def get_cache_key(self, key_name, idatastream):
        """Get cache key `key_name` from context of `idatastream`.

        If `idatastream` has a `context` and this context has a
        `key_name` attribute, the value of this attribute is
        returned. Otherwise ``None`` is returned.
        """
        context = getattr(idatastream, 'context', None)
        return getattr(context, key_name, None)


modules = [
    'odt_to_html',
    'odt_to_pdf',
    'doc_to_html',
    'doc_to_pdf',
    ]

g = globals()
transforms = []
for m in modules:
    try:
        ns = __import__(m, g, g, None)
        transforms.append(ns.register())
    except ImportError, e:
        print "Problem importing module %s : %s" % (m, e)
    except MissingBinary, e:
        print e
    except:
        import traceback
        traceback.print_exc()


def initialize(engine):
    for transform in transforms:
        engine.registerTransform(transform)
