# -*- coding: utf-8 -*-
from tg.decorators import paginate
__author__ = 'vahid'

class SmartPaginate(paginate):
    def __init__(self, name='data',
                 use_prefix=False,
                 items_per_page=10,
                 max_items_per_page=0):
        super(SmartPaginate, self).__init__(name, use_prefix, items_per_page, max_items_per_page)