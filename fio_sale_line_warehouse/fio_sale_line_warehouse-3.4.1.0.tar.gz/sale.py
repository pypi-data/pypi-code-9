# -*- coding: utf-8 -*-
"""
    sale.py

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: see LICENSE for more details.
"""
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import Pool, PoolMeta

__metaclass__ = PoolMeta
__all__ = ['SaleLine']


class SaleLine:
    __name__ = 'sale.line'

    product_type = fields.Function(
        fields.Char('Product Type'), 'on_change_with_product_type'
    )

    @classmethod
    def __setup__(cls):
        super(SaleLine, cls).__setup__()

        cls.warehouse = fields.Many2One(
            'stock.location', 'Warehouse',
            domain=[('type', '=', 'warehouse')], states={
                'invisible': (
                    (Eval('type') != 'line')
                    | (Eval('product_type') != 'goods')
                ),
                'required': (
                    (Eval('type') == 'line')
                    & (Eval('product_type') == 'goods')
                ),
                'readonly': ~Eval('_parent_sale', {}),
            }
        )
        cls.warehouse.depends.append('product_type')

    @fields.depends('type', 'product')
    def on_change_with_product_type(self, name=None):
        if self.type == 'line' and self.product:
            return self.product.type

    @staticmethod
    def default_warehouse():
        Sale = Pool().get('sale.sale')

        return Sale.default_warehouse()
