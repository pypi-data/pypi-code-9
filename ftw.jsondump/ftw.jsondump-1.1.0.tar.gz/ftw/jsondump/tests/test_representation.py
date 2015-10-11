from datetime import date
from DateTime import DateTime
from datetime import datetime
from datetime import time
from datetime import timedelta
from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IJSONRepresentation
from ftw.jsondump.representation import JSONRepresentation
from ftw.jsondump.tests.base import FtwJsondumpTestCase
from ftw.jsondump.tests.dxitem import IDXItemSchema
from ftw.jsondump.tests.helpers import asset
from ftw.jsondump.tests.helpers import asset_as_StringIO
from ftw.testing import freeze
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass
import json
import re


class TestJSONRepresentation(FtwJsondumpTestCase):

    def setUp(self):
        self.wftool = getToolByName(self.layer['portal'], 'portal_workflow')
        self.wftool.setChainForPortalTypes(('Document',),
                                           ('simple_publication_workflow',))

    def test_representation_interface(self):
        verifyClass(IJSONRepresentation, JSONRepresentation)

    def test_archetypes_document(self):
        with freeze(datetime(2010, 12, 28, 10, 55, 12)):
            document = create(
                Builder('document')
                .titled("My document")
                .having(text='<p>"S\xc3\xb6mesimple" <b>markup</b></p>',
                        effectiveDate=DateTime(),
                        demo_interger_field=42,
                        demo_float_field=42.0,
                        demo_fixedpoint_field="42.00",
                        relatedItems=[create(Builder('document').titled("Ref 1")),
                                      create(Builder('document').titled("Ref 2"))],
                        demo_file_blob_field=asset_as_StringIO('helloworld.py'),
                        demo_image_blob_field=asset_as_StringIO('empty.gif')))
            self.wftool.doActionFor(document, 'publish')
            self.wftool.doActionFor(document, 'retract')

        adapter = getMultiAdapter(
            (document, document.REQUEST), IJSONRepresentation)
        data = json.loads(adapter.json())
        expected = self.get_asset_json('archetypes_document.json')
        self.assert_structure_equal(expected, data)

    def test_dexterity_item(self):
        item = create(
            Builder('dx item')
            .titled(u'The Dexterity Item')
            .having(description=u'This is a great item!',
                    bool_field=True,
                    choice_field='Blue',
                    date_field=date(2010, 9, 8),
                    datetime_field=datetime(2012, 12, 30, 23, 59),
                    decimal_field=2.6,
                    dottedname_field='zope.schema.interfaces.IDottedName',
                    float_field=1.3,
                    list_field=[u'foo', u'bar', u'baz'],
                    richtext_field=(IDXItemSchema['richtext_field'].fromUnicode(
                        u'<p>Hello World.</p>')),
                    text_field=u'A great text.',
                    time_field=time(23, 58, 59, 1),
                    timedelta_field=timedelta(days=2, milliseconds=1, microseconds=7),
                    uri_field='http://www.python.org/foo/bar')
            .attach_image(asset('empty.gif'))
            .attach_file(asset('helloworld.py')))

        adapter = getMultiAdapter((item, item.REQUEST), IJSONRepresentation)
        data = json.loads(adapter.json())
        expected = self.get_asset_json('dexterity_item.json')
        self.assert_structure_equal(expected, data)

    def test_build_only_selected_partials(self):
        document = create(Builder('document').titled("My document"))
        adapter = getMultiAdapter((document, document.REQUEST),
                                  IJSONRepresentation)
        data = json.loads(adapter.json(only=['interfaces', 'properties']))
        self.assertItemsEqual(['_directly_provided', '_properties'], data.keys())

    def test_exclude_partials(self):
        document = create(Builder('document').titled("My document"))
        adapter = getMultiAdapter((document, document.REQUEST),
                                  IJSONRepresentation)

        data = json.loads(adapter.json()).keys()
        self.assertIn('_properties', data)
        self.assertIn('_directly_provided', data)

        data = json.loads(adapter.json(exclude=['properties'])).keys()
        self.assertNotIn('_properties', data)
        self.assertIn('_directly_provided', data)

    def test_cannot_use_only_and_exclude_simultaneously(self):
        document = create(Builder('document').titled("My document"))
        adapter = getMultiAdapter((document, document.REQUEST),
                                  IJSONRepresentation)
        with self.assertRaises(ValueError) as cm:
            adapter.json(only=['properties'], exclude=['interfaces'])

        self.assertEquals('Cannot use "only" and "exclude" simultaneously.',
                          str(cm.exception))

    def get_asset_json(self, name):
        raw = asset(name).text()

        # replace uids
        for marker, path in re.findall(r'(<<uid:([^>]*)>>)', raw):
            obj = self.layer['app'].restrictedTraverse(path.encode('utf-8'))
            raw = raw.replace(marker, obj.UID())

        return json.loads(raw)
