import re
import unittest
import xml.etree.ElementTree as ET

from bidon.data import ModelBase, ForeignModelWrapper


class Person(ForeignModelWrapper):
  attrs = dict(
    first_name=None,
    last_name=None,
    company_id=None)
  mapping = dict(
    first_name=("first_name", lambda s: s.strip()),
    last_name=("last_name", lambda s: s.strip()),
    company_id=("company", lambda d: int(d["id"])))


class Company(ModelBase):
  attrs = dict(id=None, name=None)


class PersonXML(ForeignModelWrapper):
  attrs = dict(id=None, first_name=None, last_name=None, company=None)
  mapping = dict(
    id=("id", lambda i: int(i), None),
    first_name=("first_name", ),
    last_name=("last_name", ),
    company=("company", dict(
      id=("id", int, None),
      name=("name", ))))
  submodels=dict(company=Company)


class Simple(ForeignModelWrapper):
  attrs = dict(id=None, name=None)
  mapping = dict(id=("id", lambda d: int(d)), name=("name", lambda i: i))


class DataForeignModelWrapperTestCase(unittest.TestCase):
  def test_create_raw(self):
    d = {
      "first_name": "Trey",
      "last_name": "Cucco",
      "company": {
        "id": 188,
        "name": "ACME" }}
    p = Person.create(d)
    self.assertEqual(p.first_name, "Trey")
    self.assertEqual(p.last_name, "Cucco")
    self.assertEqual(p.company_id, 188)

  def test_map(self):
    l = [dict(id=1, name="Trey Cucco"),
         dict(id=2, name="J.R.R. Tolkien"),
         dict(id=3, name="C.S. Lewis")]
    ml = list(Simple.map(l))

    self.assertEqual(len(ml), 3)
    for s in ml:
      self.assertIsInstance(s, Simple)
    self.assertEqual(ml[0].id, 1)
    self.assertEqual(ml[0].name, "Trey Cucco")
    self.assertEqual(ml[1].id, 2)
    self.assertEqual(ml[1].name, "J.R.R. Tolkien")
    self.assertEqual(ml[2].id, 3)
    self.assertEqual(ml[2].name, "C.S. Lewis")

  def test_create_xml(self):
    xmlt = """<person id="1">
      <first_name>Trey</first_name>
      <last_name>Cucco</last_name>
      <company id="1">
        <name>ACME</name>
      </company>
    </person>"""
    root = ET.fromstring(xmlt)
    p = PersonXML.create(root, mapping_format="xml")
    self.assertEqual(p.id, 1)
    self.assertEqual(p.company.id, 1)
    self.assertEqual(p.company.name, "ACME")
    self.assertEqual(p.first_name, "Trey")
    self.assertEqual(p.last_name, "Cucco")
