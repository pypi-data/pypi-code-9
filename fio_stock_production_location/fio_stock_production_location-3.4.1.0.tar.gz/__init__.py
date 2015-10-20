# -*- coding: utf-8 -*-
from trytond.pool import Pool

from production import Production


def register():
    Pool.register(
        Production,
        module='stock_production_location', type_='model'
    )
