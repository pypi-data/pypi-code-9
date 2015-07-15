import unittest
from domingo.fields import AsyncInt, Int, Float, List, Char


class FieldTests(unittest.TestCase):
    """
    Tests the various interactions amongst fields and between python data
    types and fields
    """

    def setUp(self):
        self.int_field = Int(1)

        self.float_field = Float(3.5)

        self.list_data = range(4)
        self.list_field = List(self.list_data)

        self.char_data = 'hello, this is a test'
        self.char_field = Char(self.char_data)

    def test_eq(self):
        self.assertTrue(self.list_field, self.list_data)
        self.assertEqual(self.list_field, self.list_data)

        self.assertFalse(self.int_field == self.float_field)
        self.assertTrue(self.int_field == 1.)

        self.assertEqual(self.char_field, self.char_data)
        self.assertEqual(self.char_field, Char('hello, this is a test'))
        self.assertTrue(self.char_field == self.char_data)

    def test_ne(self):
        self.assertFalse(self.list_field != self.list_data, 'list fail')
        self.assertNotEqual(self.list_field, range(10), 'list fail')

        self.assertFalse(self.int_field != 1., 'int fail')
        self.assertTrue(self.int_field != self.float_field, 'int fail')

        self.assertNotEqual(self.char_field, 'wrong')
        self.assertNotEqual(self.char_field, Char('breaking shit are we??'))
        self.assertFalse(self.char_field != self.char_data)
        self.assertTrue(self.char_field != 'fail')

    def test_multiply(self):
        self.assertEqual(self.int_field * 2, 2)
        self.assertEqual(self.int_field * self.float_field, 3.5)

    def test_divide(self):
        self.assertEqual(self.int_field / 2, 0)
        self.assertEqual(self.int_field / 2., 0.5)
        self.assertEqual(self.int_field / self.float_field, 1 / 3.5)

    def test_add(self):
        self.assertEqual(self.int_field + 1., 2)
        self.assertEqual(self.int_field + self.float_field, 4.5)

    def test_radd(self):
        self.assertEqual('before' + self.char_field, 'before' + self.char_field)
        self.assertNotEqual(self.char_field, Char('breaking shit are we??'))

    def test_subtract(self):
        self.assertEqual(self.int_field - 1., 0)
        self.assertEqual(self.int_field - self.float_field, -2.5)

    def test_lt(self):
        self.assertFalse(self.int_field < 2)
        self.assertFalse(self.int_field < 0)
        self.assertTrue(self.int_field < self.float_field)

    def test_gt(self):
        self.assertFalse(self.int_field > 2)
        self.assertTrue(self.int_field > 0)
        self.assertFalse(self.int_field > self.float_field)

    def test_ge(self):
        self.assertTrue(self.int_field >= 0)
        self.assertTrue(self.int_field >= 1.)
        self.assertFalse(self.int_field >= self.float_field)

    def test_le(self):
        self.assertFalse(self.int_field <= 0)
        self.assertTrue(self.int_field <= 1.)
        self.assertTrue(self.int_field <= self.float_field)


class AsyncIntTests(unittest.TestCase):

    def setUp(self):
        self.base_kwargs = {'owner': 'ho', 'name': 'stuff'}

    def test_init_w_nothing(self):
        self.assertRaises(
            AttributeError, AsyncInt, **self.base_kwargs
        )

    def test_init_w_condition_type(self):
        self.assertRaises(
            AttributeError, AsyncInt, condition_type="decrement",
            **self.base_kwargs
        )

    def test_init_w_condition_key(self):
        self.assertRaises(
            AttributeError, AsyncInt, condition_key='hello',
            **self.base_kwargs
        )

    def test_init_w_all_reqs(self):
        AsyncInt(
            condition_type="decrement", condition_key="hi", **self.base_kwargs
        )
