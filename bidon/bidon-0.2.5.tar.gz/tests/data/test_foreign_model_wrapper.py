import unittest
from xml.etree import ElementTree as ET

import bidon.util.transform as T
import bidon.util.convert as conv
from bidon.data import ForeignModelWrapper


class Person(ForeignModelWrapper):
  attrs = dict(first_name=None, last_name=None, company_id=None)
  transform_args = (
    None,
    dict(first_name=T.val(T.json_val("/first_name")),
         last_name=T.val(T.json_val("/last_name")),
         company_id=T.val(T.json_val("/company/id"), conv.to_int)))


class SimplePerson(ForeignModelWrapper):
  attrs = dict(id=None, name=None)
  transform_args = (
    None,
    dict(id=T.val(T.json_val("/id"), conv.to_int),
         name=T.val(T.json_val("/name"))))


class CompanyXML(ForeignModelWrapper):
  attrs = dict(id=None, name=None)


class PersonXML(ForeignModelWrapper):
  attrs = dict(id=None, first_name=None, last_name=None, company=None)
  transform_args = (
    None,
    dict(id=T.val(T.xml_attr("id"), conv.to_int),
         first_name=T.val(T.xml_text("first_name")),
         last_name=T.val(T.xml_text("last_name")),
         company=T.obj(T.xml_child("company"),
                       dict(id=T.val(T.xml_attr("id"), conv.to_int),
                            name=T.val(T.xml_text("name"))),
                       CompanyXML)))


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
    ml = list(SimplePerson.map(l))

    self.assertEqual(len(ml), 3)
    for s in ml:
      self.assertIsInstance(s, SimplePerson)
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
    p = PersonXML.create(root)
    self.assertEqual(p.id, 1)
    self.assertIsInstance(p.company, CompanyXML)
    self.assertEqual(p.company.id, 1)
    self.assertEqual(p.company.name, "ACME")
    self.assertEqual(p.first_name, "Trey")
    self.assertEqual(p.last_name, "Cucco")
