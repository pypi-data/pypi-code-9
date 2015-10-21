# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import Model


class Backend(Model):

    __prefix_key__ = 'backends'

    def as_dict(self):
        return dict(
            address=getattr(self, 'address', ''),
            port=getattr(self, 'port', 0),
            tag=getattr(self, 'tag', ''))
