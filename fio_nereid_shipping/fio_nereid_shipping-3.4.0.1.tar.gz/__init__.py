# -*- coding: utf-8 -*-
"""
    __init__.py

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: see LICENSE for details.
"""
from trytond.pool import Pool
from carrier import Carrier
from checkout import Checkout
from sale import Sale


def register():
    Pool.register(
        Checkout,
        Carrier,
        Sale,
        module='nereid_shipping', type_='model'
    )
