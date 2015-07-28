# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool
from sale import SaleLine
from product import ProductByLocationExcludeAssigned
from stock import Move


def register():
    Pool.register(
        SaleLine,
        Move,
        module='sale_available_stock', type_='model'
    )
    Pool.register(
        ProductByLocationExcludeAssigned,
        module='sale_available_stock', type_='wizard'
    )
