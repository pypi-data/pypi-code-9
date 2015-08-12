import re
import unittest

from bidon.data import ModelBase, Validation, Validator


class Person(ModelBase):
  table_name = "people"
  attrs = {
    "first_name": None,
    "last_name": None,
    "age": 0 }
  validator = Validator([
    Validation.is_present("last_name"),
    Validation.is_present("first_name")])


class DataModelBaseTestCase(unittest.TestCase):
  def test_init(self):
    p1 = Person(dict(first_name="Lucy", last_name="In the Sky With Diamonds"))
    self.assertTrue(hasattr(p1, "first_name"))
    self.assertTrue(hasattr(p1, "last_name"))
    self.assertTrue(hasattr(p1, "age"))
    p2 = Person()
    self.assertTrue(hasattr(p2, "first_name"))
    self.assertTrue(hasattr(p2, "last_name"))
    self.assertTrue(hasattr(p2, "age"))
    self.assertEqual(p2.age, 0)
    p3 = Person(id=11)
    self.assertEqual(p3.id, 11)

  def test_is_new(self):
    class C1(ModelBase):
      primary_key_name = "id"

    class C2(ModelBase):
      primary_key_name = ("parent_id", "name")

    c1 = C1()
    c2 = C2()
    self.assertTrue(c1.is_new)
    self.assertTrue(c2.is_new)
    c1.update(id=1)
    c2.update(parent_id=1, name="Hi")
    self.assertFalse(c1.is_new)
    self.assertFalse(c2.is_new)

  def test_validate(self):
    p1 = Person(dict(first_name="Eleanor", last_name="Rigby"))
    self.assertTrue(p1.validate())
    p1.first_name = None
    self.assertFalse(p1.validate())
    p1.first_name = "Eleanor"
    p1.last_name = None
    self.assertFalse(p1.validate())

  def test_error_methods(self):
    p1 = Person(dict(first_name="Mother Nature's", last_name="Son"))
    self.assertFalse(p1.has_errors)
    p1.add_error("first_name", "Isn't real")
    self.assertTrue(p1.has_errors)
    p1.clear_errors()
    self.assertFalse(p1.has_errors)

  def test_update(self):
    p1 = Person(dict(first_name="Rocky", last_name="Raccoon"))
    self.assertEqual(1, len(p1.update(dict(last_name="Balboa"))))
    self.assertEqual(p1.last_name, "Balboa")
    self.assertEqual(0, len(p1.update(dict(first_name="Rocky"))))
    self.assertEqual({"first_name", "last_name", "age"}, p1.update(first_name="A", last_name="B", age=44))
    ModelBase.strict_attrs = True
    with self.assertRaises(Exception):
      p1.update(some_unknown_attr="hihi")

  def test_to_dict(self):
    p1 = Person(dict(first_name="Mr.", last_name="Kite"))
    self.assertEqual(dict(first_name="Mr.", last_name="Kite", age=0, errors={}, updated_at=None, created_at=None, id=None), p1.to_dict())
    self.assertEqual(dict(first_name="Mr."), p1.to_dict(include_keys=["first_name"]))
    self.assertEqual(dict(first_name="Mr.", last_name="Kite", age=0), p1.to_dict(exclude_keys=["errors", "updated_at", "created_at", "id"]))

