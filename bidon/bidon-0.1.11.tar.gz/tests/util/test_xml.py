import unittest
import xml.etree.ElementTree as ET

from bidon.util.xml import transform


class UtilXMLTestCase(unittest.TestCase):
  def test_transform(self):
    tree = ET.parse("tests/fixtures/purchase-order.xml")
    root = tree.getroot()
    result = transform(root, dict(
      no="PurchaseOrderNumber",
      dt="OrderDate",
      to=("Address[@Type='Shipping']", dict(
        name=("Name", ),
        country=("Country", ))),
      items=("Items/Item", dict(no="PartNumber", name=("ProductName", )), "*")))

    self.assertEqual(result, dict(
      no="99503",
      dt="1999-10-20",
      to=dict(name="Ellen Adams", country="USA"),
      items=[
        dict(no="872-AA", name="Lawnmower"),
        dict(no="926-AA", name="Baby Monitor")
      ]))
