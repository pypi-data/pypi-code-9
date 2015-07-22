# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Frontend(object):

    __prefix_key__ = 'frontends'

    def __init__(self, port=0, protocol=''):
        self.port = port
        self.protocol = protocol

    def as_dict(self):
        return dict(
            port=self.port,
            protocol=self.protocol)
