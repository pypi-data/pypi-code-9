from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IFieldExtractor
from ftw.jsondump.tests.base import FtwJsondumpTestCase
from ftw.jsondump.tests.dxitem import IDXItemSchema
from zope.component import getMultiAdapter
import json


class TestArcheTypesPartial(FtwJsondumpTestCase):

    def test_richtext_extrator(self):
        value = IDXItemSchema['richtext_field'].fromUnicode(u'<p>A great text.</p>')
        item = create(Builder('dx item').having(richtext_field=value))

        data = {}
        field_dotted = 'ftw.jsondump.tests.dxitem.IDXItemSchema.richtext_field'
        field = IDXItemSchema['richtext_field']
        getMultiAdapter((item, item.REQUEST, field), IFieldExtractor).extract(
            'richtext_field', data, {})

        self.maxDiff = None
        self.assertDictEqual(
            {field_dotted: '<p>A great text.</p>',
             field_dotted + ':mimeType': 'text/html',
             field_dotted + ':outputMimeType': 'text/x-html-safe',
             field_dotted + ':encoding': 'utf-8'},
            data)
        self.assert_structure_equal(data, json.loads(json.dumps(data)))

    def test_no_richtext(self):
        item = create(Builder('dx item'))

        data = {}
        field_dotted = 'ftw.jsondump.tests.dxitem.IDXItemSchema.richtext_field'
        field = IDXItemSchema['richtext_field']
        getMultiAdapter((item, item.REQUEST, field), IFieldExtractor).extract(
            'richtext_field', data, {})
        self.assertDictEqual({field_dotted: None}, data)
