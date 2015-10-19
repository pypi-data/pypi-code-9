from hatcher.testing import unittest
from ..utils import AppSorter, EggNameSorter


class TestEggNameSorter(unittest.TestCase):

    def test_hashing(self):
        # Given
        egg = 'egg-0.1.2.dev4-1.egg'

        # When
        sorter1 = EggNameSorter(egg)
        sorter2 = EggNameSorter(egg)

        # Then
        self.assertEqual(sorter1, sorter2)
        self.assertEqual(hash(sorter1), hash(sorter2))

    def test_cannot_compare(self):
        # Given
        left = 'egg-1.2.0-1.egg'
        right = EggNameSorter('egg-1.2.0-1.egg')

        # When/Then
        with self.assertRaises(TypeError):
            left == right

        # When/Then
        with self.assertRaises(TypeError):
            left < right

        # When/Then
        with self.assertRaises(TypeError):
            left > right

        # When/Then
        with self.assertRaises(TypeError):
            left <= right

        # When/Then
        with self.assertRaises(TypeError):
            left >= right

    def test_equality(self):
        # Given
        left = EggNameSorter('egg-1.2.0-1.egg')
        right = EggNameSorter('egg-1.2.0-1.egg')

        # When/Then
        self.assertEqual(left, right)

        # Given
        left = EggNameSorter('egg-1.2.0-1.egg')
        right = EggNameSorter('egg-1.2-1.egg')

        # When/Then
        self.assertEqual(left, right)

        # Given
        left = EggNameSorter('egg-1.2.0-1.egg')
        right = EggNameSorter('egg-1.2.0-2.egg')

        # When/Then
        self.assertNotEqual(left, right)

        # Given
        left = EggNameSorter('egg-1.1.0-1.egg')
        right = EggNameSorter('egg-1.2.0-1.egg')

        # When/Then
        self.assertNotEqual(left, right)

        # Given
        left = EggNameSorter('egg-1.1.0-1.egg')
        right = EggNameSorter('other_egg-1.1.0-1.egg')

        # When/Then
        self.assertNotEqual(left, right)

    def test_less_than(self):
        # Given
        left = EggNameSorter('egg-1.2.0-1.egg')
        right = EggNameSorter('egg-1.2.0-1.egg')

        # When/Then
        self.assertTrue(left <= right)
        self.assertTrue(left >= right)
        self.assertFalse(left < right)
        self.assertFalse(left > right)

        # Given
        left = EggNameSorter('egg-1.2.0-1.egg')
        right = EggNameSorter('egg-1.2.0-2.egg')

        # When/Then
        self.assertTrue(left <= right)
        self.assertTrue(left < right)
        self.assertFalse(left >= right)
        self.assertFalse(left > right)

        # Given
        left = EggNameSorter('egg-1.2.0-2.egg')
        right = EggNameSorter('egg-1.2.1-1.egg')

        # When/Then
        self.assertTrue(left <= right)
        self.assertTrue(left < right)
        self.assertFalse(left >= right)
        self.assertFalse(left > right)

        # Given
        left = EggNameSorter('a-1.2.0-1.egg')
        right = EggNameSorter('b-1.2.0-1.egg')

        # When/Then
        self.assertTrue(left <= right)
        self.assertTrue(left < right)
        self.assertFalse(left >= right)
        self.assertFalse(left > right)

        # Given
        left = EggNameSorter('a-1.2.0-1.egg')
        right = EggNameSorter('b-1.1.0-1.egg')

        # When/Then
        self.assertTrue(left <= right)
        self.assertTrue(left < right)
        self.assertFalse(left >= right)
        self.assertFalse(left > right)


class TestAppSorter(unittest.TestCase):

    def test_hashing(self):
        # Given
        name = 'mayavi'
        version = '2.3.4-1'
        python_tag = 'cp27'

        # When
        sorter1 = AppSorter(name, version, python_tag)
        sorter2 = AppSorter(name, version, python_tag)

        # Then
        self.assertEqual(sorter1, sorter2)
        self.assertEqual(hash(sorter1), hash(sorter2))

    def test_cannot_compare(self):
        # Given
        left = EggNameSorter('egg-1.2.0-1.egg')
        right = AppSorter('mayavi', '2.3.4-1', 'cp27')

        # When/Then
        with self.assertRaises(TypeError):
            left == right

        # When/Then
        with self.assertRaises(TypeError):
            left < right

        # When/Then
        with self.assertRaises(TypeError):
            left > right

        # When/Then
        with self.assertRaises(TypeError):
            left <= right

        # When/Then
        with self.assertRaises(TypeError):
            left >= right

    def test_equality(self):
        # Given
        left = AppSorter('app', '1.2.0-1', 'cp27')
        right = AppSorter('app', '1.2.0-1', 'cp27')

        # When/Then
        self.assertEqual(left, right)

        # Given
        left = AppSorter('app', '1.2.0-1', 'cp27')
        right = AppSorter('app', '1.2-1', 'cp27')

        # When/Then
        self.assertEqual(left, right)

        # Given
        left = AppSorter('app', '1.2.0-1', 'cp27')
        right = AppSorter('app', '1.2.0-2', 'cp27')

        # When/Then
        self.assertNotEqual(left, right)

        # Given
        left = AppSorter('app', '1.1.0-1', 'cp27')
        right = AppSorter('app', '1.2.0-1', 'cp27')

        # When/Then
        self.assertNotEqual(left, right)

        # Given
        left = AppSorter('app', '1.1.0-1', 'cp27')
        right = AppSorter('other_app', '1.1.0-1', 'cp27')

        # When/Then
        self.assertNotEqual(left, right)

        # Given
        left = AppSorter('app', '1.2.0-1', 'cp27')
        right = AppSorter('app', '1.2.0-1', 'cp34')

        # When/Then
        self.assertNotEqual(left, right)

    def test_less_than(self):
        # Given
        left = AppSorter('app', '1.2.0-1', 'cp27')
        right = AppSorter('app', '1.2.0-1', 'cp27')

        # When/Then
        self.assertTrue(left <= right)
        self.assertTrue(left >= right)
        self.assertFalse(left < right)
        self.assertFalse(left > right)

        # Given
        left = AppSorter('app', '1.2.0-1', 'cp27')
        right = AppSorter('app', '1.2.0-2', 'cp27')

        # When/Then
        self.assertTrue(left <= right)
        self.assertTrue(left < right)
        self.assertFalse(left >= right)
        self.assertFalse(left > right)

        # Given
        left = AppSorter('app', '1.2.0-2', 'cp27')
        right = AppSorter('app', '1.2.1-1', 'cp27')

        # When/Then
        self.assertTrue(left <= right)
        self.assertTrue(left < right)
        self.assertFalse(left >= right)
        self.assertFalse(left > right)

        # Given
        left = AppSorter('a', '1.2.0-1', 'cp27')
        right = AppSorter('b', '1.2.0-1', 'cp27')

        # When/Then
        self.assertTrue(left <= right)
        self.assertTrue(left < right)
        self.assertFalse(left >= right)
        self.assertFalse(left > right)

        # Given
        left = AppSorter('a', '1.2.0-1', 'cp27')
        right = AppSorter('b', '1.1.0-1', 'cp27')

        # When/Then
        self.assertTrue(left <= right)
        self.assertTrue(left < right)
        self.assertFalse(left >= right)
        self.assertFalse(left > right)

        # Given
        left = AppSorter('app', '1.2.0-1', 'cp27')
        right = AppSorter('app', '1.2.0-1', 'cp34')

        # When/Then
        self.assertTrue(left <= right)
        self.assertTrue(left < right)
        self.assertFalse(left >= right)
        self.assertFalse(left > right)
