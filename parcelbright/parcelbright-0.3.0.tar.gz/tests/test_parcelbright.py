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

from schematics.exceptions import ModelValidationError

import parcelbright

if not hasattr(unittest, 'skipUnless'):
    import unittest2 as unittest


class TestParcelBright(unittest.TestCase):

    def test_shipment_entity(self):
        parcel = parcelbright.Parcel({
            'width': 10, 'height': 10, 'length': 10, 'weight': 1
        })
        from_address = parcelbright.Address({
            'name': 'office', 'postcode': 'NW1 0DU', 'town': 'London',
            'phone': '07800000000', 'country_code': 'GB',
            'line1': '19 Mandela Street'
        })
        to_address = parcelbright.Address({
            'name': 'John Doe', 'postcode': 'E2 8RS', 'town': 'London',
            'phone': '07411111111', 'country_code': 'GB',
            'line1': '19 Mandela Street'
        })
        shipment = parcelbright.Shipment({
            'customer_reference': '123455667', 'estimated_value': 100,
            'contents': 'books', 'pickup_date': '2025-01-29',
            'parcel': parcel, 'from_address': from_address,
            'to_address': to_address
        })
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

        parcel = parcelbright.Parcel({
            'width': 10, 'height': 10, 'length': 10, 'weight': 1
        })
        from_address = parcelbright.Address({
            'name': 'office', 'postcode': 'NW1 0DU', 'town': 'London',
            'phone': '07800000000', 'country_code': 'GB',
            'line1': '19 Mandela Street'
        })
        to_address = parcelbright.Address({
            'name': 'John Doe', 'postcode': 'E2 8RS', 'town': 'London',
            'phone': '07411111111', 'country_code': 'GB',
            'line1': '19 Mandela Street'
        })
        shipment = parcelbright.Shipment({
            'customer_reference': '123455667', 'estimated_value': 100,
            'contents': 'books', 'pickup_date': '2025-01-29',
            'parcel': parcel, 'from_address': from_address,
            'to_address': to_address
        })
        shipment.create()

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

        parcel = parcelbright.Parcel({
            'width': 10, 'height': 10, 'length': 10, 'weight': 1
        })
        from_address = parcelbright.Address({
            'name': 'office', 'postcode': 'NW1 0DU', 'town': 'London',
            'phone': '07800000000', 'country_code': 'GB',
            'line1': '19 Mandela Street'
        })
        to_address = parcelbright.Address({
            'name': 'John Doe', 'postcode': 'E2 8RS', 'town': 'London',
            'phone': '07411111111', 'country_code': 'GB',
            'line1': '19 Mandela Street'
        })
        shipment = parcelbright.Shipment({
            'customer_reference': '123455667', 'estimated_value': 100,
            'contents': 'books', 'pickup_date': '2025-01-29',
            'parcel': parcel, 'from_address': from_address,
            'to_address': to_address
        })
        shipment.create()

        self.assertTrue(isinstance(shipment.rates, list))
        self.assertEqual(shipment.state, 'incomplete')

        pickup_date = (datetime.now() + timedelta(days=4)).strftime(
            '%Y-%m-%d'
        )
        shipment.book(
            shipment.rates[0].code, pickup_date=pickup_date
        )
        self.assertEqual(shipment.state, 'completed')
        self.assertEqual(shipment.pickup_date.isoformat(), pickup_date)

        shipment.cancel()
        self.assertEqual(shipment.state, 'cancelled')

    def test_address_validation(self):
        # invalid name
        with self.assertRaises(ModelValidationError):
            parcelbright.Address({
                'name': '', 'postcode': 'NW1 0DU',
                'town': 'london', 'phone': '07800000000',
                'line1': '12 Mandela Street',
                'country_code': 'GB'
            }).validate()

        # invalid postcode
        with self.assertRaises(ModelValidationError):
            parcelbright.Address({
                'name': 'name', 'postcode': '',
                'town': 'london', 'phone': '07800000000',
                'line1': '12 Mandela Street',
                'country_code': 'GB'
            }).validate()

        # invalid town
        with self.assertRaises(ModelValidationError):
            parcelbright.Address({
                'name': 'name', 'postcode': 'NW1 0DU',
                'town': '', 'phone': '07800000000',
                'line1': '12 Mandela Street',
                'country_code': 'GB'
            }).validate()

        # invalid line1
        with self.assertRaises(ModelValidationError):
            parcelbright.Address({
                'name': 'name', 'postcode': 'NW1 0DU',
                'town': 'london', 'phone': '07800000000',
                'line1': '',
                'country_code': 'GB'
            }).validate()

        # invalid phone
        with self.assertRaises(ModelValidationError):
            parcelbright.Address({
                'name': 'name', 'postcode': 'NW1 0DU',
                'town': 'london', 'phone': '',
                'line1': '12 Mandela Street',
                'country_code': 'GB'
            }).validate()

        with self.assertRaises(ModelValidationError):
            parcelbright.Address({
                'name': 'name', 'postcode': 'NW1 0DU',
                'town': 'london', 'phone': '078000000xx',
                'line1': '12 Mandela Street',
                'country_code': 'GB'
            }).validate()

        # invalid country_code
        with self.assertRaises(ModelValidationError):
            parcelbright.Address({
                'name': 'name', 'postcode': 'NW1 0DU',
                'town': 'london', 'phone': '07800000000',
                'line1': '12 Mandela Street',
                'country_code': ''
            }).validate()


if __name__ == '__main__':
    unittest.main()
