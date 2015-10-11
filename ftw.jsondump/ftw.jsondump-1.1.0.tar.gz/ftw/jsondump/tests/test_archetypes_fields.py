from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IFieldExtractor
from ftw.jsondump.tests.base import FtwJsondumpTestCase
from ftw.jsondump.tests.helpers import asset_as_StringIO
from ftw.jsondump.tests.helpers import EMPTY_GIF_BASE64
from ftw.jsondump.tests.helpers import HELLOWORLD_BASE64
from plone.app.testing import TEST_USER_ID
from plone.uuid.interfaces import IUUID
from zope.component import getMultiAdapter
import json


class TestArcheTypesPartial(FtwJsondumpTestCase):

    def get_path(self, obj):
        return '/'.join(obj.getPhysicalPath())

    def test_stringfield_extrator(self):
        title = "My document"
        document = create(Builder('document').titled(title))

        data = {}
        config = {}
        field = document.Schema()['title']
        getMultiAdapter((document, document.REQUEST, field),
                        IFieldExtractor).extract('title', data, config)

        self.assertEquals({'title': title},
                          data)
        self.assert_structure_equal(json.loads(json.dumps(data)), data)

    def test_textfield_extractor(self):
        text = "<p>Some simple <b>markup</b></p>"
        document = create(Builder('document').having(text=text))

        data = {}
        config = {}
        field = document.Schema()['text']
        getMultiAdapter((document, document.REQUEST, field),
                        IFieldExtractor).extract('text', data, config)

        self.assertEquals({'text': text, 'text:mimetype': 'text/html'},
                          data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_datetime_field_extractor(self):
        startdate = DateTime()
        document = create(Builder('document').having(effectiveDate=startdate))

        data = {}
        config = {}
        field = document.Schema()['effectiveDate']
        getMultiAdapter((document, document.REQUEST, field),
                        IFieldExtractor).extract('effectiveDate', data, config)

        self.assertEquals({'effectiveDate:date': str(startdate)},
                          data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_lines_field_extractor(self):
        creators = ['hans', 'peter', 'heiri']
        document = create(Builder('document').having(creators=creators))

        data = {}
        config = {}
        field = document.Schema()['creators']

        getMultiAdapter((document, document.REQUEST, field),
                        IFieldExtractor).extract('creators', data, config)

        self.assertEquals({'creators': creators + [TEST_USER_ID]},
                          data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_integer_field_extractor(self):

        integer = 42
        document = create(Builder('document')
                          .having(demo_interger_field=integer))

        data = {}
        config = {}
        field = document.Schema()['demo_interger_field']

        getMultiAdapter(
            (document, document.REQUEST, field),
            IFieldExtractor).extract('demo_interger_field', data, config)

        self.assertEquals({'demo_interger_field': integer},
                          data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_float_field_extractor(self):

        float_ = 42.0
        document = create(Builder('document')
                          .having(demo_float_field=float_))

        data = {}
        config = {}
        field = document.Schema()['demo_float_field']

        getMultiAdapter(
            (document, document.REQUEST, field),
            IFieldExtractor).extract('demo_float_field', data, config)

        self.assertEquals({'demo_float_field': float_},
                          data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_fixedpoint_field_extractor(self):

        fixedpoint = "42.00"
        document = create(Builder('document')
                          .having(demo_fixedpoint_field=fixedpoint))

        data = {}
        config = {}
        field = document.Schema()['demo_fixedpoint_field']

        getMultiAdapter(
            (document, document.REQUEST, field),
            IFieldExtractor).extract('demo_fixedpoint_field', data, config)

        self.assertEquals({'demo_fixedpoint_field': fixedpoint},
                          data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_reference_field_extractor(self):
        ref_document1 = create(Builder('document')
                               .titled("Ref 1"))
        ref_document2 = create(Builder('document')
                               .titled("Ref 2"))
        document = create(Builder('document')
                          .having(relatedItems=[ref_document1, ref_document2]))

        data = {}
        config = {}
        field = document.Schema()['relatedItems']

        getMultiAdapter(
            (document, document.REQUEST, field),
            IFieldExtractor).extract('relatedItems', data, config)

        self.assertEquals(
            {'relatedItems:path': [
                self.get_path(ref_document1), self.get_path(ref_document2)],
             'relatedItems:uuid': [
                IUUID(ref_document1), IUUID(ref_document2)]},
            data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_single_reference_field_extractor(self):
        ref_document = create(Builder('document')
                              .titled("Ref 1"))
        document = create(Builder('document')
                          .having(demo_single_ref_field=ref_document))

        data = {}
        config = {}
        field = document.Schema()['demo_single_ref_field']

        getMultiAdapter(
            (document, document.REQUEST, field),
            IFieldExtractor).extract('demo_single_ref_field', data, config)

        self.assertEquals(
            {'demo_single_ref_field:path': self.get_path(ref_document),
             'demo_single_ref_field:uuid': IUUID(ref_document)},
            data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_empty_single_reference_field_extractor(self):
        document = create(Builder('document'))

        data = {}
        config = {}
        field = document.Schema()['demo_single_ref_field']

        getMultiAdapter(
            (document, document.REQUEST, field),
            IFieldExtractor).extract('demo_single_ref_field', data, config)

        self.assertEquals(
            {'demo_single_ref_field:path': '',
             'demo_single_ref_field:uuid': ''},
            data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_empty_multivalue_reference_field_extractor(self):
        document = create(Builder('document'))

        data = {}
        config = {}
        field = document.Schema()['relatedItems']

        getMultiAdapter(
            (document, document.REQUEST, field),
            IFieldExtractor).extract('relatedItems', data, config)

        self.assertEquals(
            {'relatedItems:path': '',
             'relatedItems:uuid': ''},
            data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_computed_field_extractor(self):
        document = create(Builder('document'))

        data = {}
        config = {}
        field = document.Schema()['demo_computed_field']

        getMultiAdapter(
            (document, document.REQUEST, field),
            IFieldExtractor).extract('demo_computed_field', data, config)

        self.assertEquals({'demo_computed_field': 'Computed value'},
                          data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_boolean_field_extractor(self):

        boolean = True
        document = create(Builder('document')
                          .having(demo_bool_field=boolean))

        data = {}
        config = {}
        field = document.Schema()['demo_bool_field']

        getMultiAdapter(
            (document, document.REQUEST, field),
            IFieldExtractor).extract('demo_bool_field', data, config)

        self.assertEquals({'demo_bool_field': boolean},
                          data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_file_field_extractor(self):
        document = create(Builder('document')
                          .having(demo_file_field=asset_as_StringIO('helloworld.py')))

        data = {}
        config = {}
        field = document.Schema()['demo_file_field']

        getMultiAdapter(
            (document, document.REQUEST, field),
            IFieldExtractor).extract('demo_file_field', data, config)

        self.assertEquals({'demo_file_field:file': HELLOWORLD_BASE64,
                           'demo_file_field:filename': 'helloworld.py',
                           'demo_file_field:size': 20,
                           'demo_file_field:mimetype': 'text/x-python'},
                          data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_file_field_extractor_WITHOUT_file_data(self):
        document = create(Builder('document')
                          .having(demo_file_field=asset_as_StringIO('helloworld.py')))

        data = {}
        config = {'filedata': False}
        field = document.Schema()['demo_file_field']

        getMultiAdapter(
            (document, document.REQUEST, field),
            IFieldExtractor).extract('demo_file_field', data, config)

        self.assertEquals({'demo_file_field:filename': 'helloworld.py',
                           'demo_file_field:size': 20,
                           'demo_file_field:mimetype': 'text/x-python'},
                          data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_image_field_extractor(self):
        document = create(Builder('document')
                          .having(demo_image_field=asset_as_StringIO('empty.gif')))

        data = {}
        config = {}
        field = document.Schema()['demo_image_field']

        getMultiAdapter(
            (document, document.REQUEST, field),
            IFieldExtractor).extract('demo_image_field', data, config)

        self.assertEquals({'demo_image_field:file': EMPTY_GIF_BASE64,
                           'demo_image_field:filename': 'empty.gif',
                           'demo_image_field:size': 42,
                           'demo_image_field:mimetype': 'image/gif'},
                          data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_file_blob_field_extractor(self):
        document = create(Builder('document')
                          .having(demo_file_blob_field=asset_as_StringIO('helloworld.py')))

        data = {}
        config = {}
        field = document.Schema()['demo_file_blob_field']

        getMultiAdapter(
            (document, document.REQUEST, field),
            IFieldExtractor).extract('demo_file_blob_field', data, config)

        self.assertEquals({'demo_file_blob_field:file': HELLOWORLD_BASE64,
                           'demo_file_blob_field:filename': 'helloworld.py',
                           'demo_file_blob_field:size': 20,
                           'demo_file_blob_field:mimetype': 'text/x-python'},
                          data)
        self.assertEquals(json.loads(json.dumps(data)), data)

    def test_image_blob_field_extractor(self):
        document = create(Builder('document')
                          .having(demo_image_blob_field=asset_as_StringIO('empty.gif')))

        data = {}
        config = {}
        field = document.Schema()['demo_image_blob_field']

        getMultiAdapter(
            (document, document.REQUEST, field),
            IFieldExtractor).extract('demo_image_blob_field', data, config)

        self.assertEquals({'demo_image_blob_field:file': EMPTY_GIF_BASE64,
                           'demo_image_blob_field:filename': 'empty.gif',
                           'demo_image_blob_field:size': 42,
                           'demo_image_blob_field:mimetype': 'image/gif'},
                          data)
        self.assertEquals(json.loads(json.dumps(data)), data)
