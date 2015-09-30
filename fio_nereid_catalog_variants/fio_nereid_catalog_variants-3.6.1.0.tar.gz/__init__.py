# -*- coding: utf-8 -*-
from trytond.pool import Pool
from product import Template, Product, ProductVariationAttributes, \
    ProductAttribute


def register():
    Pool.register(
        Template,
        Product,
        ProductVariationAttributes,
        ProductAttribute,
        module='nereid_catalog_variants', type_='model'
    )
