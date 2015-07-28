# -*- coding: utf-8 -*-
"""
    tests/test_client.py

"""
import os
import unittest

import trytond.tests.test_tryton
from trytond.modules.shipping_dpd.dpd_client import DPDClient, DPDException


class TestClientAPI(unittest.TestCase):
    '''
    Test Client API
    '''

    def setUp(self):
        """
        Set up data used in the tests.
        this method is called before each test function execution.
        """
        self.server = os.environ.get(
            'DPD_SERVER', 'https://public-ws-stage.dpd.com'
        )
        self.login_service_wsdl = self.server + \
            '/services/LoginService/V2_0?wsdl'
        self.shipment_service_wsdl = self.server + \
            '/services/ShipmentService/V3_2?wsdl'
        self.depot_data_service_wsdl = self.server + \
            '/services/DepotDataService/V1_0/?wsdl'
        self.parcel_shop_finder_service_wsdl = self.server + \
            '/services/ParcelShopFinderService/V3_0?wsdl'
        self.username = os.environ['DPD_USERNAME']
        self.password = os.environ['DPD_PASSWORD']

    def test_0010_correct_auth(self):
        """
        Test if the auth works!
        """
        client = DPDClient(
            self.login_service_wsdl, self.shipment_service_wsdl,
            self.depot_data_service_wsdl, self.parcel_shop_finder_service_wsdl,
            self.username, self.password
        )
        result = client.get_auth()
        self.assert_(result.authToken)
        self.assert_(result.depot)

    def test_0020_wrong_auth(self):
        """
        Test if the wrong auth fails!
        """
        client = DPDClient(
            self.login_service_wsdl, self.shipment_service_wsdl,
            self.depot_data_service_wsdl, self.parcel_shop_finder_service_wsdl,
            self.username, 'not' + self.password
        )
        with self.assertRaises(DPDException):
            client.get_auth()

    @unittest.skip('TODO: Fix depot data fetching')
    def test_0030_get_depot_data(self):
        """
        Test if depot_data api is working
        """
        client = DPDClient(
            self.login_service_wsdl, self.shipment_service_wsdl,
            self.depot_data_service_wsdl, self.parcel_shop_finder_service_wsdl,
            self.username, self.password
        )
        client.get_depot_data(country_code='DE', zip='63741')


def suite():
    """
    Define suite
    """
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestClientAPI)
    )
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
