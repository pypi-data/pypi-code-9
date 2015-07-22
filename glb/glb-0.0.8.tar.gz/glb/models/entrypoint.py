# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Entrypoint(object):

    __prefix_key__ = 'entripoints'

    def __init__(self, domain='', port=0, protocol='',
                 cipher='', certificate={}):
        self.domain = domain
        self.port = port
        self.protocol = protocol
        self.cipher = cipher
        self.certificate = certificate

    def as_dict(self):
        return dict(
            domain=self.domain,
            port=self.port,
            protocol=self.protocol,
            cipher=self.cipher,
            certificate=self.certificate)
