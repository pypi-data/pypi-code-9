# -*- coding: utf-8 -*-

from django.test.utils import setup_test_environment
setup_test_environment()
from django.test.client import Client
client = Client()
from django.core.urlresolvers import reverse
from django.test import TestCase


class WritebackTests(TestCase):

    def test_post_writeback_form(self):
        """
        """
        response = self.client.post(reverse('writeback_message_create'))
        self.assertEqual(response.status_code, 200)
