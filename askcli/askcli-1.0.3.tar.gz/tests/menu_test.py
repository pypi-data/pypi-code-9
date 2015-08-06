# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from askcli import Menu, Item
from mock import patch

class TestMenu(unittest.TestCase):


    def setUp(self):
        self.VALID_CHOICES = ['menu 1', Item('a', 'testing'), 'tata']
        self.valid_menu = Menu(self.VALID_CHOICES, 'valid', True)


    def test_init_fail_whithout_param(self):
        with self.assertRaises(TypeError):
            Menu()

    def test_init_fail_whith_bad_choice_type(self):
        with self.assertRaises(ValueError):
            Menu('not list type')

    def test_init_fail_whith_bad_element_in_choice(self):
        choice = ['menu 1', Item('a', 'testing'), 1]
        with self.assertRaises(ValueError):
            Menu(choice)

    def test_init(self):
        m1 = Menu(self.VALID_CHOICES)
        m2 = Menu(self.VALID_CHOICES, title="titre")
        m3 = Menu(self.VALID_CHOICES, title="titre", case=True)

        valid_choice = [
            Item('1', 'menu 1'),
            Item('a', 'testing'),
            Item('3', 'tata')
        ]

        self.assertEqual(len(m1._choice), 3)
        self.assertEqual(len(m2._choice), 3)
        self.assertEqual(len(m3._choice), 3)

        self.assertEqual(m1._choice, valid_choice)
        self.assertEqual(m2._choice, valid_choice)
        self.assertEqual(m3._choice, valid_choice)

        self.assertFalse(m1.case)
        self.assertFalse(m2.case)
        self.assertTrue(m3.case)

        self.assertEqual(m1.title, '')
        self.assertEqual(m2.title, 'titre')
        self.assertEqual(m3.title, 'titre')

        self.assertEqual(m1.choose, -1)
        self.assertEqual(m2.choose, -1)
        self.assertEqual(m3.choose, -1)

    def test_repr(self):
        valid_ret = "<askcli.menu 3 choice>"
        self.assertEqual(self.valid_menu.__repr__(), valid_ret)

    def test_to_str(self):

        valid_ret = "> valid"
        valid_ret +="\n   1 - menu 1"
        valid_ret +="\n   a - testing"
        valid_ret +="\n   3 - tata"

        self.assertEqual(self.valid_menu.__str__(), valid_ret)

    def test_fail_key_is_ok(self):
        
        self.valid_menu.case = False
        self.assertFalse(self.valid_menu.key_is_ok('q'))
        self.assertFalse(self.valid_menu.key_is_ok('Q'))
        self.valid_menu.case = True
        self.assertFalse(self.valid_menu.key_is_ok('q'))
        self.assertFalse(self.valid_menu.key_is_ok('Q'))

    def test_valid_key_is_ok(self):
        
        self.valid_menu.case = False
        self.assertTrue(self.valid_menu.key_is_ok('1'))
        self.assertTrue(self.valid_menu.key_is_ok('a'))
        self.assertTrue(self.valid_menu.key_is_ok('A'))
        self.assertTrue(self.valid_menu.key_is_ok('3'))
        self.valid_menu.case = True
        self.assertTrue(self.valid_menu.key_is_ok('1'))
        self.assertTrue(self.valid_menu.key_is_ok('a'))
        self.assertFalse(self.valid_menu.key_is_ok('A'))
        self.assertTrue(self.valid_menu.key_is_ok('3'))

    def test_fail_set_choice(self):

        with self.assertRaises(ValueError):
            self.valid_menu._set_choice('q')

        self.assertEqual(self.valid_menu._choose_index, -1)


    def test_get_choosen_text_not_launch(self):
        self.assertEqual(self.valid_menu.get_choosen_text(), '')


    def test_valid_set_choice(self):
        self.valid_menu._set_choice('1')
        self.assertEqual(self.valid_menu.choose, '1')
        self.assertEqual(self.valid_menu._choose_index, 0)
        self.valid_menu._set_choice('a')
        self.assertEqual(self.valid_menu.choose, 'a')
        self.assertEqual(self.valid_menu._choose_index, 1)
        self.valid_menu._set_choice('3')
        self.assertEqual(self.valid_menu.choose, '3')
        self.assertEqual(self.valid_menu._choose_index, 2)

    def test_get_choosen_text(self):
        self.valid_menu._set_choice('3')
        self.assertEqual(self.valid_menu.get_choosen_text(), 'tata')

    @patch('askcli.Menu.launch', return_value='ok')
    def test_launch(self, input):
        m = Menu(['yes','no'])
        self.assertEqual(m.launch(), 'ok')


if __name__ == '__main__':
    unittest.main()
