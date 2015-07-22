# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Slave(object):

    __prefix_key__ = 'slaves'

    def __init__(self, address='', sync_time=''):
        self.address = address
        self.sync_time = sync_time

    def as_dict(self):
        return dict(address=self.address,
                    sync_time=self.sync_time)
