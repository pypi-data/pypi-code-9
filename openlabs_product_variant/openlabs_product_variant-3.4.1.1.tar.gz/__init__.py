# -*- coding: utf-8 -*-
"""
    __init__.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool
from product import Template, Product


def register():
    Pool.register(
        Template,
        Product,
        module='product_variant', type_='model'
    )
