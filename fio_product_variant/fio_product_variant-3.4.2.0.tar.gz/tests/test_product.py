# -*- coding: utf-8 -*-
"""
    tests/test_product.py

"""
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, USER, DB_NAME, CONTEXT
from trytond.transaction import Transaction


class TestProduct(unittest.TestCase):
    def setUp(self):
        trytond.tests.test_tryton.install_module('product_variant')

        self.ProductTemplate = POOL.get('product.template')
        self.Product = POOL.get('product.product')
        self.Uom = POOL.get('product.uom')

    def test_0010_use_variant_lp_and_cp(self):
        """Since we have moved list price and cost price to variant, any logic
        which goes for product lp and cp should raise an exception.
        """
        with Transaction().start(DB_NAME, USER, context=CONTEXT):

            uom, = self.Uom.search([('symbol', '=', 'u')])
            template, = self.ProductTemplate.create([{
                'name': 'Test_Product',
                'type': 'goods',
                'default_uom': uom.id,
            }])

            product, = self.Product.create([{
                'template': template.id,
                'list_price': 5000,
                'cost_price': 4000,
            }])

            with self.assertRaises(Exception):
                product.template.list_price

            with self.assertRaises(Exception):
                product.template.cost_price
