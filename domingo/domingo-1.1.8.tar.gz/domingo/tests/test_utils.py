import unittest
from domingo.utils import classproperty


class TestModel(object):
    "A class for use only in this test file"

    _test = 'yo'

    @classproperty
    def test(cls):
        return 'hello'

    @classproperty
    def test2(cls):
        return cls._test


class ClassProperyTests(unittest.TestCase):

    def test_class_usage(self):

        self.assertEqual('hello', TestModel.test)
        self.assertEqual('yo', TestModel.test2)

    def test_instance_usage(self):

        self.assertEqual('hello', TestModel().test)
        self.assertEqual('yo', TestModel().test2)

    def test_inheritance_usage(self):

        class Inherit(TestModel):
            _test = 'works!'

        self.assertEqual('hello', Inherit().test)
        self.assertEqual('works!', Inherit().test2)
