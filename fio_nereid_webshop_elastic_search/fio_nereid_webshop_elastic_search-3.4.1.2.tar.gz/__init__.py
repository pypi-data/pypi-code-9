# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool
from product import Product, Template, ProductAttribute
from website import Website


def register():
    Pool.register(
        Product,
        ProductAttribute,
        Template,
        Website,
        module='nereid_webshop_elastic_search', type_='model'
    )
