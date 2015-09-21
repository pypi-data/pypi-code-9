import re
import unittest
from collections import namedtuple

from bidon.data import ModelBase, Validation, Validator, ModelAccess

from tests import get_model_access


class Person(ModelBase):
  table_name = "people"
  attrs = {
    "first_name": None,
    "last_name": None,
    "age": 0}
  validator = Validator([
    Validation.is_unique("first_name", scope=["last_name"])])


class DataValidationTestCase(unittest.TestCase):
  def setUp(self):
    self.model = Person(first_name="Lord", last_name="Voldemort", age=68)

  def test_is_present(self):
    v = Validation.is_present("first_name")
    self.assertTrue(v.is_valid(self.model)[0])
    self.model.first_name = None
    self.assertFalse(v.is_valid(self.model)[0])

  def test_is_length(self):
    v = Validation.is_length("first_name", min_length=2)
    self.assertTrue(v.is_valid(self.model)[0])
    self.model.first_name = "L"
    self.assertFalse(v.is_valid(self.model)[0])
    self.model.first_name = None
    self.assertFalse(v.is_valid(self.model)[0])
    v = Validation.is_length("first_name", present_optional=True)
    self.assertTrue(v.is_valid(self.model)[0])
    v = Validation.is_length("last_name", max_length=5)
    self.assertFalse(v.is_valid(self.model)[0])

  def test_matches(self):
    v = Validation.matches("last_name", re.compile(r"^[A-Z]"))
    self.assertTrue(v.is_valid(self.model)[0])
    self.model.last_name = self.model.last_name.lower()
    self.assertFalse(v.is_valid(self.model)[0])

  def test_is_unique(self):
    with get_model_access() as ma:
      self.assertTrue(self.model.validate(ma))
      ma.insert_model(self.model)
      self.assertTrue(self.model.validate(ma))
      m2 = Person(first_name="Lord", last_name="Voldemort")
      self.assertFalse(m2.validate(ma))

      class P2(ModelBase):
        table_name = "people"
        attrs = dict(first_name=None, last_name=None, age=0)
        validator = Validator([
          Validation.is_unique("first_name", comparison_operators=[" = "])
        ])

      p2 = P2(first_name="Lord", last_name="Churchhill")
      self.assertFalse(p2.validate(ma))
      p2.first_name = "Winston"
      self.assertTrue(p2.validate(ma))

      ma.rollback()

  def test_numeric(self):
    v = Validation.is_numeric("age")
    self.assertTrue(v.is_valid(self.model)[0])

    v = Validation.is_numeric("age", numtype="int")
    self.model.age = "68.5"
    self.assertFalse(v.is_valid(self.model)[0])

    v = Validation.is_numeric("age", numtype="int", min=0, max=120)
    self.model.age = -1
    self.assertFalse(v.is_valid(self.model)[0])
    self.model.age = 121
    self.assertFalse(v.is_valid(self.model)[0])
    self.model.age = 68
    self.assertTrue(v.is_valid(self.model)[0])

    self.model.age = None
    self.assertFalse(v.is_valid(self.model)[0])

  def test_date(self):
    DTT = namedtuple("dtt", ["date", "datetime"])
    dtt = DTT("2014-01-01", "2014-01-01 13:45:15.0")
    vd = Validation.is_date("date")
    vdt = Validation.is_datetime("datetime")

    self.assertTrue(vd.is_valid(dtt)[0])
    self.assertTrue(vdt.is_valid(dtt)[0])

  def test_is_in(self):
    v = Validation.is_in("first_name", { "john", "paul", "george", "ringo" })
    self.assertFalse(v.is_valid(self.model)[0])
    self.model.first_name = "ringo"
    self.assertTrue(v.is_valid(self.model)[0])

  def test_filter(self):
    class M(ModelBase):
      attrs = dict(first_name=None, last_name=None)

    m1 = M(first_name="trey", last_name=None)
    m2 = M(first_name=None, last_name=None)
    v = Validation.is_present("last_name").add_filter(lambda m: m.first_name is not None)

    self.assertFalse(v.validate(m1))
    self.assertTrue(v.validate(m2))
