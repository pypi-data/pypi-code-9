# -*- coding: utf-8 -*-
"""
    stock.py

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction
from trytond.model import fields
from trytond.pyson import Eval


__metaclass__ = PoolMeta
__all__ = ['Move']


class Move:
    "Stock Move"
    __name__ = "stock.move"

    available_qty = fields.Function(
        fields.Float(
            'Available Quantity', digits=(16, Eval('unit_digits', 2)),
            depends=['unit_digits']
        ), 'on_change_with_available_qty'
    )

    @fields.depends('product', 'planned_date', 'from_location')
    def on_change_with_available_qty(self, name=None):
        """
        Returns the available quantity
        """
        Date = Pool().get('ir.date')

        if not (self.product and self.from_location):
            return

        if self.from_location.type != 'storage':
            return

        date = self.planned_date or Date.today()
        date = max(date, Date.today())

        location = self.from_location

        with Transaction().set_context(
                locations=[location.id], stock_date_end=date,
                stock_assign=True):

            if date <= Date.today():
                return self.product.quantity
            else:
                return self.product.forecast_quantity
