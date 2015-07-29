#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_parcelbright
----------------------------------

Tests for `parcelbright` module.
"""

from datetime import datetime, timedelta
import os
import unittest

import parcelbright

if not hasattr(unittest, 'skipUnless'):
    import unittest2 as unittest


class TestParcelBright(unittest.TestCase):

    def test_parcel_entity(self):
        p = parcelbright.Parcel(
            width=10, height=10, length=10, weight=1
        )
        self.assertEqual(p.dict(), {
            'width': 10, 'height': 10, 'length': 10, 'weight': 1,
        })
        self.assertEqual(
            p.__repr__(),
            '<Parcel [width=10, height=10, length=10, weight=1]>'
        )

    def test_parcel_entity_with_protected_fields(self):
        p = parcelbright.Parcel(
            width=10, height=10, length=10, weight=1
        )
        p._protected = True
        p.__private = True
        self.assertEqual(p.dict(), {
            'width': 10, 'height': 10, 'length': 10, 'weight': 1,
        })

    def test_address_entity(self):
        a = parcelbright.Address(
            name='office', postcode='AAA AAA', town='London',
            phone='12341234', country_code='GB', line1='line'
        )
        self.assertEqual(a.dict(), {
            'name': 'office', 'postcode': 'AAA AAA', 'town': 'London',
            'phone': '12341234', 'country_code': 'GB', 'line1': 'line'
        })
        self.assertEqual(
            a.__repr__(),
            '<Address [name=office, postcode=AAA AAA, town=London, line1=line, country_code=GB]>'  # NOQA
        )

    def test_shipment_entity(self):
        parcel = parcelbright.Parcel(
            length=10, width=10, height=10, weight=1
        )
        from_address = parcelbright.Address(
            name="office", postcode="NW1 0DU",
            town="London", phone="07800000000",
            line1="19 Mandela Street",
            country_code="GB"
        )
        to_address = parcelbright.Address(
            name="John Doe", postcode="E2 8RS",
            town="London", phone="07411111111",
            line1="19 Mandela Street",
            country_code="GB"
        )
        shipment = parcelbright.Shipment(
            customer_reference='123455667', estimated_value=100,
            contents='books', pickup_date='2025-01-29',
            parcel=parcel, from_address=from_address,
            to_address=to_address
        )
        self.assertEqual(
            shipment.__repr__(),
            '<Shipment [id=None, contents=books, state=unknown]>'
        )
        with self.assertRaises(parcelbright.ShipmentNotCompletedException):
            shipment.track()

    @unittest.skipUnless(
        'PARCELBRIGHT_TEST_API_KEY' in os.environ,
        """Skip integrations test unless environment variable
        PARCELBRIGHT_TEST_API_KEY is not set"""
    )
    def test_rate(self):
        parcelbright.api_key = os.environ.get('PARCELBRIGHT_TEST_API_KEY')
        parcelbright.sandbox = True
        parcel = parcelbright.Parcel(
            length=10, width=10, height=10, weight=1
        )
        from_address = parcelbright.Address(
            name="office", postcode="NW1 0DU",
            town="London", phone="07800000000",
            line1="19 Mandela Street",
            country_code="GB"
        )
        to_address = parcelbright.Address(
            name="John Doe", postcode="E2 8RS",
            town="London", phone="07411111111",
            line1="19 Mandela Street",
            country_code="GB"
        )
        shipment = parcelbright.Shipment.create(
            customer_reference='123455667', estimated_value=100,
            contents='books', pickup_date='2025-01-29',
            parcel=parcel, from_address=from_address,
            to_address=to_address
        )
        self.assertTrue(isinstance(shipment.rates, list))
        self.assertEqual(shipment.state, 'incomplete')

        found_shipment = parcelbright.Shipment.find(shipment.id)
        self.assertEqual(shipment.id, found_shipment.id)

        with self.assertRaises(parcelbright.NotFound):
            parcelbright.Shipment.find('invalid')

        found_shipment.book(found_shipment.rates[0]['code'])
        self.assertEqual(found_shipment.state, 'completed')

        events = found_shipment.track()
        self.assertEqual(len(events), 1)

        found_shipment.cancel()
        self.assertEqual(found_shipment.state, 'cancelled')

    @unittest.skipUnless(
        'PARCELBRIGHT_TEST_API_KEY' in os.environ,
        """Skip integrations test unless environment variable
        PARCELBRIGHT_TEST_API_KEY is not set"""
    )
    def test_book_with_custom_pickup_date(self):
        parcelbright.api_key = os.environ.get('PARCELBRIGHT_TEST_API_KEY')
        parcelbright.sandbox = True
        parcel = parcelbright.Parcel(
            length=10, width=10, height=10, weight=1
        )
        from_address = parcelbright.Address(
            name="office", postcode="NW1 0DU",
            town="London", phone="07800000000",
            line1="19 Mandela Street",
            country_code="GB"
        )
        to_address = parcelbright.Address(
            name="John Doe", postcode="E2 8RS",
            town="London", phone="07411111111",
            line1="19 Mandela Street",
            country_code="GB"
        )
        shipment = parcelbright.Shipment.create(
            customer_reference='123455667', estimated_value=100,
            contents='books', pickup_date='2025-01-29',
            parcel=parcel, from_address=from_address,
            to_address=to_address
        )
        self.assertTrue(isinstance(shipment.rates, list))
        self.assertEqual(shipment.state, 'incomplete')

        pickup_date = (datetime.now() + timedelta(days=4)).strftime(
            '%Y-%m-%d'
        )
        shipment.book(
            shipment.rates[0]['code'], pickup_date=pickup_date
        )
        self.assertEqual(shipment.state, 'completed')
        self.assertEqual(shipment.pickup_date, pickup_date)

        shipment.cancel()
        self.assertEqual(shipment.state, 'cancelled')

if __name__ == '__main__':
    unittest.main()
