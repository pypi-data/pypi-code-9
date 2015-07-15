import time
import unittest
from domingo.backends.base import QueryError
from domingo.models import AsyncModel
from domingo.fields import Char, Int, List, Set


class TestModel(AsyncModel):

    unique_on = ['char_field']

    char_field = Char()
    int_field = Int()
    list_field = List()
    set_field = Set()
    second_char_field = Char()


class SecondTestModel(TestModel):

    unique_on = ['char_field', 'int_field']


class QueryTests(unittest.TestCase):

    def setUp(self):
        self.instance = TestModel(char_field='hello')
        self.instance.save()

    @classmethod
    def tearDownClass(cls):
        TestModel.store.collection.drop()
        SecondTestModel.store.collection.drop()

    def test_unique_on_works(self):
        "create a second instance and then make sure the count is still one"
        instance = TestModel(char_field='hello')
        instance.save()
        self.assertEqual(
            TestModel.store.collection.count(),
            1
        )

        instance = TestModel(char_field='hello')
        instance._fields['int_field'].set(1)
        instance.save()
        self.assertEqual(
            TestModel.store.collection.count(),
            1
        )

    def test_unique_on_with_get_works(self):
        """
        We require that getting the instance from mongo after creating it, and
        then saving it again does not create duplicates
        """
        instance = TestModel.get(char_field='hello')
        instance.save()
        self.assertEqual(
            TestModel.store.collection.count(),
            1
        )

        instance._fields['int_field'].set(1)
        instance.save()

        # instance = TestModel.get(char_field='hello')
        # instance.save()

        TestModel.create(data=TestModel(char_field='hello'))
        self.assertEqual(
            TestModel.store.collection.count(),
            1
        )

    def test_unique_on_not_instatiated_raises_error(self):
        incomplete_instance = SecondTestModel(char_field='asdfasdf')
        self.assertRaises(QueryError, incomplete_instance.save)
        incomplete_instance = SecondTestModel(int_field=1)
        self.assertRaises(QueryError, incomplete_instance.save)

    def test_default_values_are_not_saved_to_the_collection(self):
        "how about that for a long ass name...."
        document = TestModel.store.collection.find_one({'char_field': 'hello'})
        self.assertTrue(
            'int_field' not in document,
            '"int_field" is in the document! Mongo is saving default values '
            'in the database that are not lists.'
        )
        self.assertTrue(
            'list_field' in document,
            '"list_field" is NOT in the document! Mongo should instatiate '
            'iterables in the database upon creation of the document.'
        )
        self.assertTrue(
            'set_field' in document,
            '"set_field" is NOT in the document! Mongo should instatiate '
            'iterables in the database upon creation of the document.'
        )

    def test_modified_and_created_are_different(self):
        original_doc = TestModel.store.collection.find_one(
            {'char_field': 'hello'}
        )

        instance = TestModel(char_field='hello')
        instance.save()
        doc = TestModel.store.collection.find_one({'char_field': 'hello'})

        self.assertEqual(original_doc['created'], doc['created'])
        self.assertNotEqual(doc['created'], doc['modified'])

        self.assertEqual(instance.modified, doc['modified'])
        self.assertLess(original_doc['modified'], doc['modified'])

    def test_upated_on_single_field_works(self):
        # ensure second_char_field isn't in the docuemnt
        doc = TestModel.store.collection.find_one({'char_field': 'hello'})
        self.assertTrue('second_char_field' not in doc)
        instance = TestModel(
            char_field='hello', second_char_field='yo', int_field=2
        )
        instance.save()
        doc = TestModel.store.collection.find_one({'char_field': 'hello'})
        self.assertEqual(doc['second_char_field'], instance.second_char_field)
        self.assertEqual(doc['int_field'], instance.int_field)

        updated_instance = TestModel(char_field='hello', int_field=10)
        updated_instance.save()
        doc = TestModel.store.collection.find_one({'char_field': 'hello'})
        self.assertEqual(doc['second_char_field'], instance.second_char_field)
        self.assertEqual(doc['int_field'], updated_instance.int_field)

    def test_unique_on_index_is_present(self):
        index_info = TestModel.store.collection.index_information()
        self.assertTrue('unique_on' in index_info)
        self.assertIsNotNone(index_info['unique_on'].get('key'))
        self.assertEquals(index_info['unique_on']['key'], [('char_field', 1)])
