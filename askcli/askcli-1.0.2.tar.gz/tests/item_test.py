# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from askcli import Item
from askcli.item import YES, NO, OUI, NON


class TestItem(unittest.TestCase):


    def setUp(self):
        self.valid_item = Item('a', 'menu 1')


    def test_init_fail_whithout_param(self):
        with self.assertRaises(TypeError):
            Item()

        with self.assertRaises(TypeError):
            Item("t")

    def test_init(self):
        i1 = Item('a', 'menu 1')
        i2 = Item('b', 'menu 2', True)


        self.assertFalse(i1.activate)
        self.assertTrue(i2.activate)
        self.assertEqual(i1.txt, 'menu 1')
        self.assertEqual(i2.txt, 'menu 2')
        self.assertEqual(i1.key, 'a')
        self.assertEqual(i2.key, 'b')

    def test_repr(self):
        valid_ret = "<askcli.Item : a - menu 1>"
        self.assertEqual(self.valid_item.__repr__(), valid_ret)

    def test_to_str(self):

        valid_ret = " a - menu 1"
        valid_ret_2 = ">a - menu 1"

        self.assertEqual(self.valid_item.__str__(), valid_ret)
        self.valid_item.activate = True
        self.assertEqual(self.valid_item.__str__(), valid_ret_2)

    def test_eq_item(self):
        valid_item_doublon = Item('a', 'menu 1')
        not_eq_item = Item('b', 'menu b')
        not_eq_item_2 = Item('A', 'menu A')
        
        self.assertTrue((valid_item_doublon == self.valid_item))
        self.assertFalse((not_eq_item == self.valid_item))
        self.assertFalse((not_eq_item_2 == self.valid_item))
        self.assertFalse(('a' == self.valid_item))

    def test_load_var(self):
        self.assertEqual(YES.key, 'Y')
        self.assertEqual(YES.txt, 'Yes')
        self.assertEqual(NO.key, 'N')
        self.assertEqual(NO.txt, 'No')
        self.assertEqual(OUI.key, 'O')
        self.assertEqual(OUI.txt, 'Oui')
        self.assertEqual(NON.key, 'N')
        self.assertEqual(NON.txt, 'Non')


if __name__ == '__main__':
    unittest.main()
