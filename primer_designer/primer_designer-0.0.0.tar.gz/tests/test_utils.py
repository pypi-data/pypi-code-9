import unittest

from primer_designer import utils


class UtilsTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_check_if_is_fasta_file(self):
        self.assertTrue(utils.is_fasta("Ca2.fas"))
        self.assertTrue(utils.is_fasta("Ca2.FAS"))
        self.assertTrue(utils.is_fasta("Ca2.fst"))
        self.assertTrue(utils.is_fasta("Ca2.fasta"))
        self.assertTrue(utils.is_fasta("Ca2.fa"))
        self.assertFalse(utils.is_fasta("Ca2.fata"))
