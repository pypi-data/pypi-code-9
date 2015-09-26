# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool
from sale import Sale


def register():
    Pool.register(
        Sale,
        module='sale_confirmation_email', type_='model'
    )
