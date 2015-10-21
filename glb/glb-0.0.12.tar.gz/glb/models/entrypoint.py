# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import Model


class Entrypoint(Model):

    __prefix_key__ = 'entripoints'

    def as_dict(self):
        return dict(
            domain=getattr(self, 'domain', ''),
            port=getattr(self, 'port', 0),
            protocol=getattr(self, 'protocol', ''),
            cipher=getattr(self, 'cipher', ''),
            certificate=getattr(self, 'certificate', {}))
