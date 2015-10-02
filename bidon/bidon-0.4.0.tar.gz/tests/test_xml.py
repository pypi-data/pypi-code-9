import os
import unittest

from bidon.xml import ElementPuller
from tests import TEST_ROOT


class ElementPullerTestCase(unittest.TestCase):
  def test_element_puller(self):
    books = []
    ep = ElementPuller("book", lambda p: books.append(p))
    with open(os.path.join(TEST_ROOT, "fixtures", "books.xml")) as rf:
      ep.parse(rf)
    self.assertEqual(books[0].attrib["id"], "bk101")
    self.assertEqual(books[0].find("./description").text,
                     "An in-depth look at creating applications with XML.")
