# -*- coding: utf-8 -*-

import unittest

from cwr.parser.encoder.dictionary import WriterDictionaryEncoder
from cwr.interested_party import Writer
from cwr.other import IPIBaseNumber

"""
Writer to dictionary encoding tests.

The following cases are tested:
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class TestWriterDictionaryEncoding(unittest.TestCase):
    def setUp(self):
        self._encoder = WriterDictionaryEncoder()

    def test_encoded(self):
        ipi_base = IPIBaseNumber('I', 229, 7)

        data = Writer(ip_n='ABC15',
                      personal_number='ABC1234',
                      ipi_name_n=14107338,
                      ipi_base_n=ipi_base,
                      writer_first_name='NAME',
                      writer_last_name='LAST NAME',
                      tax_id=923703412)

        encoded = self._encoder.encode(data)

        self.assertEqual('ABC15', encoded['ip_n'])
        self.assertEqual('ABC1234', encoded['personal_number'])
        self.assertEqual(14107338, encoded['ipi_name_n'])
        self.assertEqual('NAME', encoded['writer_first_name'])
        self.assertEqual('LAST NAME', encoded['writer_last_name'])
        self.assertEqual(923703412, encoded['tax_id'])

        self.assertEqual('I', encoded['ipi_base_n']['header'])
        self.assertEqual(229, encoded['ipi_base_n']['id_code'])
        self.assertEqual(7, encoded['ipi_base_n']['check_digit'])
