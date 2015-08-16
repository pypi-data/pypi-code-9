# -*- coding: utf-8 -*-
from django.test import SimpleTestCase, TestCase

from .client import IpApiClient
from .middleware import CheckCountryCodeMiddleware


class DjangoIpApiClientTest(SimpleTestCase):
    """bin/frontend-dev test ipapi --testrunner=ipapi.test_runner.WithoutDb"""

    def setUp(self):
        self.client = IpApiClient()

    def test_get_US_country_code(self):
        self.assertEqual(self.client.get_country_code('208.80.152.201'), 'US')

    def test_get_PL_country_code(self):
        self.assertEqual(self.client.get_country_code('83.10.128.162'), 'PL')


# class CheckCountryCodeMiddlewareeTest(TestCase):
#     """bin/frontend-dev test ipapi --testrunner=ipapi.test_runner.WithoutDb"""
#
#     def setUp(self):
#         self.middleware = CheckCountryCodeMiddleware()
#         self.request = Mock()
#         self.request.session = {}
