# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import Model


class Slave(Model):

    __prefix_key__ = 'slaves'

    def as_dict(self):
        return dict(address=getattr(self, 'address', ''),
                    haproxy_version=getattr(self, 'haproxy_version', ''),
                    nginx_version=getattr(self, 'nginx_version', ''))
