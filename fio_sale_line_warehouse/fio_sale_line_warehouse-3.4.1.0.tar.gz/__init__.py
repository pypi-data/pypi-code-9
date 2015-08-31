# -*- coding: utf-8 -*-
"""
    __init__.py

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: see LICENSE for details.
"""
from trytond.pool import Pool

from sale import SaleLine


def register():
    Pool.register(
        SaleLine,
        module='sale_line_warehouse', type_='model'
    )
