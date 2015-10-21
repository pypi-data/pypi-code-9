# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import Model


class Frontend(Model):

    __prefix_key__ = 'frontends'

    def as_dict(self):
        return dict(
            port=getattr(self, 'port', 0),
            protocol=getattr(self, 'protocol', ''))
