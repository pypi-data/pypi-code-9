# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Backend(object):

    __prefix_key__ = 'backends'

    def __init__(self, tag='', address='', port=80):
        self.tag = tag
        self.address = address
        self.port = port

    def as_dict(self):
        return dict(
            tag=self.tag,
            address=self.address,
            port=int(self.port))
