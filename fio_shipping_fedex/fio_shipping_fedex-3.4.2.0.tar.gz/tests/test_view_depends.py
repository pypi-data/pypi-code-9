# -*- coding: utf-8 -*-
"""
    tests/test_view_depends.py

"""


class TestViewDepends:

    def test_views(self):
        "Test all tryton views"

        from trytond.tests.test_tryton import test_view
        test_view('shipping_fedex')

    def test_depends(self):
        "Test missing depends on fields"

        from trytond.tests.test_tryton import test_depends
        test_depends()
