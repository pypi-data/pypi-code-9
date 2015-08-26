# -*- coding: utf-8 -*-

from django.http import HttpRequest
from django.test import TestCase


class NavTestCase(TestCase):
    """
    Nav Test
    """
    def test_nav(self):
        request = HttpRequest()
        pass
