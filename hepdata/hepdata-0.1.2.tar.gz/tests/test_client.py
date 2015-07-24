#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_client
----------------------------------

Tests for `hepdata.client` module.
"""

import unittest

from hepdata import client
from hepdata import exceptions


class TestClient(unittest.TestCase):

    def test_url(self):
        c = client.GiftsClient("AABBCC")

        self.assertEqual(
            c._get_url("profiles"),
            "http://automatch.matchinggifts.com/profiles/xml/AABBCC/",
        )

        self.assertEqual(
            c._get_url("profiles", 1234),
            "http://automatch.matchinggifts.com/profiles/xml/AABBCC/1234/",
        )

        self.assertEqual(
            c._get_url("profiles", 1234, city="Arlington, VA"),
            "http://automatch.matchinggifts.com/profiles/xml/AABBCC/1234/?city=Arlington%2C+VA",
        )

    def test_clean_data(self):
        data = {u'companies': {u'company': [{u'city': u'San Antonio', u'last_updated': u'11/20/2014', u'name': u'USAA United Services Automobile Association', u'company_id': u'22170000', u'state': u'TX', u'subsidiary_id': None, u'subsidiary': u'false'}, {u'city': u'San Antonio', u'last_updated': u'11/20/2014', u'name': u'USAA', u'company_id': u'22170000', u'state': u'TX', u'subsidiary_id': u'62559', u'subsidiary': u'true'}, {u'city': u'San Antonio', u'last_updated': u'11/20/2014', u'name': u'USAA Federal Savings Bank', u'company_id': u'22170000', u'state': u'TX', u'subsidiary_id': u'54463', u'subsidiary': u'true'}], u'@count': u'3', u'@name': u'usaa'}}
        self.assertEqual(client.clean_data(data), data)

    def test_singular_data(self):
        data = {u'companies': {u'company': {u'city': u'Bentonville', u'last_updated': u'10/28/2014', u'name': u'Walmart', u'company_id': u'97730000', u'state': u'AR', u'subsidiary_id': u'51836', u'subsidiary': u'true'}, u'@count': u'1', u'@name': u'walmart'}}
        self.assertTrue(isinstance(data['companies']['company'], dict))
        self.assertTrue(isinstance(client.clean_data(data)['companies']['company'], list))


if __name__ == '__main__':
    unittest.main()
