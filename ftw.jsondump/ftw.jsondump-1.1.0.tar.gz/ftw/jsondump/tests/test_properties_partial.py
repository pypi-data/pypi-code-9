from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IPartial
from ftw.jsondump.tests.base import FtwJsondumpTestCase
from zope.component import getMultiAdapter
import json


class TestPropertiesPartial(FtwJsondumpTestCase):

    def test_properties_partial(self):
        document = create(Builder('document').titled('A Title'))

        document.manage_addProperty('a_boolean', True, 'boolean')
        document.manage_addProperty('a_date', '2014/12/12 00:00:00 GMT+1', 'date')
        document.manage_addProperty('a_float', '42.0', 'float')
        document.manage_addProperty('a_int', 42, 'int')
        document.manage_addProperty('a_long', 42, 'long')
        document.manage_addProperty('a_list', ['A', 'B', 'C'], 'lines')
        document.manage_addProperty('a_text', 'Some text', 'text')

        # XXX: Property types, token, selection, multiple selections are not
        # going to be tested, since I have no idea how the work.

        partial = getMultiAdapter((document, document.REQUEST), IPartial,
                                  name="properties")
        config = {}
        data = partial(config)

        self.maxDiff = None
        self.assertEquals({'_properties':
                           [
                               ['title', 'A Title', 'string'],
                               ['a_boolean', True, 'boolean'],
                               ['a_date', '2014/12/12 00:00:00 GMT+1', 'date'],
                               ['a_float', 42.0, 'float'],
                               ['a_int', 42, 'int'],
                               ['a_long', 42, 'long'],
                               ['a_list', ['A', 'B', 'C'], 'lines'],
                               ['a_text', 'Some text', 'text']]},
                          data)

        self.assert_structure_equal(json.loads(json.dumps(data)), data)
