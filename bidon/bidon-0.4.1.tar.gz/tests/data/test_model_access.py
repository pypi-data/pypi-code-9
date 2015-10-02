import unittest

from bidon.data import ModelBase, ModelAccess

from tests import get_model_access


class Person(ModelBase):
  table_name = "people"
  attrs = {
    "first_name": None,
    "last_name": None,
    "age": 0 }


class PersonThing(ModelBase):
  table_name = "peoples_things"
  primary_key_name = ["person_id", "thing_id"]
  primary_key_is_auto = False
  attrs = {
    "person_id": None,
    "thing_id": None,
    "quantity": 0}


class DataModelAccessTestCase(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.mab = get_model_access()
    cls.mab.open()

  @classmethod
  def tearDownClass(cls):
    cls.mab.rollback()
    cls.mab.close()

  def test_find_model(self):
    p = self.mab.find_model(Person, dict(first_name="Yours"))
    self.assertIsNotNone(p)
    self.assertIsInstance(p, Person)
    self.assertEqual(p.first_name, "Yours")

  def test_find_all_models(self):
    ps = list(self.mab.find_all_models(Person, "last_name like 'T%'"))
    self.assertEqual(len(ps), 2)
    self.assertIsInstance(ps[0], Person)
    self.assertEqual(ps[0].last_name[0], "T")

  def test_page_models(self):
    ps, count = self.mab.page_models(Person, (0, 4), order_by="id")
    self.assertEqual(count, 11)
    self.assertEqual(len(ps), 4)
    self.assertEqual([1, 2, 3, 4], [p.id for p in ps])

  def test_find_model_by_id(self):
    pt = self.mab.find_model_by_id(PersonThing, [1, 1])
    self.assertEqual(pt.person_id, 1)
    self.assertEqual(pt.thing_id, 1)
    self.assertEqual(pt.quantity, 1)
    p = self.mab.find_model_by_id(Person, 1)

  def test_refresh_model(self):
    with get_model_access() as mab:
      pt = mab.find_model(Person, "1=1")
      nn = "aabbccdd"
      mab.update(Person.table_name, dict(first_name=nn), dict(id=pt.id))
      self.assertNotEqual(pt.first_name, nn)
      self.assertEqual(mab.refresh_model(pt, False).first_name, nn)
      self.assertNotEqual(pt.first_name, nn)
      mab.refresh_model(pt, True)
      self.assertEqual(pt.first_name, nn)
      mab.rollback()

  def test_update_model(self):
    with get_model_access() as mab:
      p1 = mab.find_model_by_id(Person, 1)
      ua = p1.updated_at
      self.assertNotEqual(p1.first_name, "Minerva")
      updatedattrs = p1.update(dict(first_name="Minerva", last_name="McGonagall"))
      mab.update_model(p1, include_keys=updatedattrs)
      if mab.core.supports_returning_syntax:
        self.assertNotEqual(ua, p1.updated_at)
      p2 = mab.find_model_by_id(Person, 1)
      self.assertEqual(p2.first_name, "Minerva")
      self.assertEqual(p2.last_name, "McGonagall")
      mab.rollback()

  def test_insert_model(self):
    with get_model_access() as mab:
      p1 = Person(dict(first_name="Albus", last_name="Dumbledore", age=115))
      self.assertIsNone(p1.id)
      mab.insert_model(p1)
      self.assertIsNotNone(p1.id)
      self.assertIsNotNone(p1.created_at)
      p2 = mab.find_model_by_id(Person, p1.id)
      self.assertEqual(p1.first_name, p2.first_name)
      self.assertEqual(p1.last_name, p2.last_name)
      self.assertEqual(p1.age, p2.age)
      mab.rollback()

  def test_delete_model(self):
    with get_model_access() as mab:
      pc = mab.count("people")
      mab.delete_model(Person(id=11))
      self.assertEqual(pc - 1, mab.count("people"))
      self.assertIsNone(mab.find_model_by_id(Person, 11))

      ptc = mab.count("peoples_things")
      mab.delete_model(PersonThing(person_id=1, thing_id=1))
      self.assertEqual(ptc - 1, mab.count("peoples_things"))
      self.assertIsNone(mab.find_model_by_id(PersonThing, [1, 1]))

      mab.delete_model(PersonThing, [1, 2])
      self.assertEqual(ptc - 2, mab.count("peoples_things"))
      self.assertIsNone(mab.find_model_by_id(PersonThing, [1, 1]))

      mab.rollback()
