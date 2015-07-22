# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Balancer(object):

    __prefix_key__ = 'balancers'

    def __init__(self, name, frontend={}, backends=[], entrypoints=[]):
        self.name = name
        self.frontend = frontend
        self.backends = backends
        self.entrypoints = entrypoints

    def as_dict(self):
        return dict(
            name=self.name,
            frontend=self.frontend.as_dict() if self.frontend else {},
            backends=[b.as_dict() for b in self.backends],
            entrypoints=[e.as_dict() for e in self.entrypoints])
