# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from askcli import AskBool, Item


class TestAskBool(unittest.TestCase):


    def setUp(self):
        self.valid_aks_bool = AskBool('testing', 'Valid', 'Invalid', 'V', 'I', True)

    def test_init_fail_whithout_param(self):
        with self.assertRaises(TypeError):
            a = AskBool()

    def test_init_minimal(self):
        a = AskBool('confirm')

        self.assertEqual(a.desc, 'confirm')
        self.assertEqual(a.valid.key, 'Y')
        self.assertEqual(a.valid.txt, 'Yes')
        self.assertEqual(a.invalid.key, 'N')
        self.assertEqual(a.invalid.txt, 'No')
        self.assertTrue(a.required)
        self.assertFalse(a.default)
        self.assertIsNone(a.choosen)

    
    def test_init_with_item(self):
        valid = Item('y', 'Yes')
        invalid = Item('n', 'No')
        a = AskBool('testing', valid, invalid)

        self.assertEqual(a.desc, 'testing')
        self.assertEqual(a.valid.key, 'y')
        self.assertEqual(a.valid.txt, 'Yes')
        self.assertEqual(a.invalid.key, 'n')
        self.assertEqual(a.invalid.txt, 'No')
        self.assertTrue(a.required)
        self.assertFalse(a.default)
        self.assertIsNone(a.choosen)

    def test_init_without_item(self):
        a = AskBool('testing', 'Yes', 'No')

        self.assertEqual(a.desc, 'testing')
        self.assertEqual(a.valid.key, 'Y')
        self.assertEqual(a.valid.txt, 'Yes')
        self.assertEqual(a.invalid.key, 'N')
        self.assertEqual(a.invalid.txt, 'No')
        self.assertTrue(a.required)
        self.assertFalse(a.default)
        self.assertIsNone(a.choosen)

        a = AskBool('testing', 'Yes', 'No', 'a', 'b')
        self.assertEqual(a.desc, 'testing')
        self.assertEqual(a.valid.key, 'a')
        self.assertEqual(a.valid.txt, 'Yes')
        self.assertEqual(a.invalid.key, 'b')
        self.assertEqual(a.invalid.txt, 'No')
        self.assertTrue(a.required)
        self.assertFalse(a.default)
        self.assertIsNone(a.choosen)

    def test_init_optional_filed(self):
        a = AskBool('testing', 'Yes', 'No', 'a', 'b', False, True)
        self.assertEqual(a.desc, 'testing')
        self.assertEqual(a.valid.key, 'a')
        self.assertEqual(a.valid.txt, 'Yes')
        self.assertEqual(a.invalid.key, 'b')
        self.assertEqual(a.invalid.txt, 'No')
        self.assertFalse(a.required)
        self.assertTrue(a.default)
        self.assertIsNone(a.choosen)

    def test_repr(self):
        valid = "<askcli.AskBool : testing  [V/I]>"
        self.assertEqual(self.valid_aks_bool.__repr__(), valid)

    def test_to_str(self):
        valid = "testing  [V/I] : "
        self.assertEqual(self.valid_aks_bool.__str__(), valid)


    def test_valid_list(self):
        valid_list = self.valid_aks_bool._get_valid_array()
        self.assertEqual(len(valid_list), 2)

        self.assertEqual(valid_list[0], 'valid')
        self.assertEqual(valid_list[1], 'v')


    def test_invalid_list(self):
        invalid_list = self.valid_aks_bool._get_invalid_array()
        self.assertEqual(len(invalid_list), 2)

        self.assertEqual(invalid_list[0], 'invalid')
        self.assertEqual(invalid_list[1], 'i')

    def test_key_is_valid(self):
        keys_ok = ['i', 'I', 'V', 'v', 'valid', 'Valid', 'InvAlid', 'invalid']
        keys_fail = ['y', 'yes', 'n', 'non']
        for key in  keys_ok:
            self.assertTrue(self.valid_aks_bool.key_is_valid(key))

        for key in keys_fail:
            self.assertFalse(self.valid_aks_bool.key_is_valid(key))

    def test_set_choice(self):
        a = AskBool('testing', 'Valid', 'Invalid', 'V', 'I', True)
        
        keys_fail = ['y', 'yes', 'n', 'non']
        keys_true = ['V', 'V', 'valid', 'Valid']
        keys_false = ['I', 'i', 'invalid', 'InValid']

        for key in keys_fail:
            with self.assertRaises(ValueError):
                a.set_choice(key)
            self.assertIsNone(a.choosen)


        for key in keys_true:
            a.set_choice(key)
            self.assertTrue(a.choosen)

        for key in keys_false:
            a.set_choice(key)
            self.assertFalse(a.choosen)

    def test_get_resp(self):
        a = AskBool('testing', 'Valid', 'Invalid', 'V', 'I', True)

        with self.assertRaises(Exception):
            self.get_resp()

        a.set_choice('V')
        self.assertTrue(a.get_resp())

        a.set_choice('I')
        self.assertFalse(a.get_resp())

    def test_get_text(self):
        a = AskBool('testing', 'Valid', 'Invalid', 'V', 'I', True)

        self.assertEqual('', a.get_text())

        a.set_choice('v')
        self.assertEqual(a.get_text(), "Valid")

        a.set_choice('i')
        self.assertEqual(a.get_text(), "Invalid")






if __name__ == '__main__':
    unittest.main()
