# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool
from wishlist import NereidUser, Wishlist, Product, \
    ProductWishlistRelationship


def register():
    Pool.register(
        NereidUser,
        Wishlist,
        Product,
        ProductWishlistRelationship,
        module='nereid_wishlist', type_='model'
    )
