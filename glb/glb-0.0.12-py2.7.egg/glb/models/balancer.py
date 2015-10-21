# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import Model


class Balancer(Model):

    __prefix_key__ = 'balancers'

    def as_dict(self):
        return dict(
            name=getattr(self, 'name', ''),
            frontend=getattr(self, 'frontend', {}),
            backends=getattr(self, 'backends', []),
            entrypoints=getattr(self, 'entrypoints', []))
