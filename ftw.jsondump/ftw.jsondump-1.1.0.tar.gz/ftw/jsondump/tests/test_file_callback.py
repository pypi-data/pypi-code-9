from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IJSONRepresentation
from ftw.jsondump.tests.base import FtwJsondumpTestCase
from ftw.jsondump.tests.helpers import asset
from ftw.jsondump.tests.helpers import asset_as_StringIO
from zope.component import getMultiAdapter


class TestFileCallback(FtwJsondumpTestCase):

    def test_archetypes_file_field(self):
        document = create(Builder('document')
                          .having(demo_file_field=asset_as_StringIO('helloworld.py')))
        representation = getMultiAdapter((document, document.REQUEST), IJSONRepresentation)
        representation.json(file_callback=self.recording_file_callback(), filedata=False)
        self.assert_file_callback(context=document,
                                  key='demo_file_field',
                                  fieldname='demo_file_field',
                                  data='print "Hello World"\n',
                                  filename='helloworld.py',
                                  mimetype='text/x-python')

    def test_archetypes_file_blob_field(self):
        document = create(Builder('document')
                          .having(demo_file_blob_field=asset_as_StringIO('helloworld.py')))
        representation = getMultiAdapter((document, document.REQUEST), IJSONRepresentation)
        representation.json(file_callback=self.recording_file_callback(), filedata=False)
        self.assert_file_callback(context=document,
                                  key='demo_file_blob_field',
                                  fieldname='demo_file_blob_field',
                                  data='print "Hello World"\n',
                                  filename='helloworld.py',
                                  mimetype='text/x-python')

    def test_archetypes_image_field(self):
        document = create(Builder('document')
                          .having(demo_image_field=asset_as_StringIO('empty.gif')))
        representation = getMultiAdapter((document, document.REQUEST), IJSONRepresentation)
        representation.json(file_callback=self.recording_file_callback(), filedata=False)
        self.assert_file_callback(context=document,
                                  key='demo_image_field',
                                  fieldname='demo_image_field',
                                  filename='empty.gif',
                                  mimetype='image/gif')

    def test_archetypes_image_blob_field(self):
        document = create(Builder('document')
                          .having(demo_image_blob_field=asset_as_StringIO('empty.gif')))
        representation = getMultiAdapter((document, document.REQUEST), IJSONRepresentation)
        representation.json(file_callback=self.recording_file_callback(), filedata=False)
        self.assert_file_callback(context=document,
                                  key='demo_image_blob_field',
                                  fieldname='demo_image_blob_field',
                                  filename='empty.gif',
                                  mimetype='image/gif')

    def test_dexterity_namedfile_field(self):
        item = create(Builder('dx item').attach_file(asset('helloworld.py')))
        representation = getMultiAdapter((item, item.REQUEST), IJSONRepresentation)
        representation.json(file_callback=self.recording_file_callback(), filedata=False)
        self.assert_file_callback(context=item,
                                  key='ftw.jsondump.tests.dxitem.IDXItemSchema.file_field',
                                  fieldname='file_field',
                                  data='print "Hello World"\n',
                                  filename='helloworld.py',
                                  mimetype='text/x-python')

    def test_dexterity_namedimage_field(self):
        item = create(Builder('dx item').attach_image(asset('empty.gif')))
        representation = getMultiAdapter((item, item.REQUEST), IJSONRepresentation)
        representation.json(file_callback=self.recording_file_callback(), filedata=False)
        self.assert_file_callback(context=item,
                                  key='ftw.jsondump.tests.dxitem.IDXItemSchema.image_field',
                                  fieldname='image_field',
                                  filename='empty.gif',
                                  mimetype='image/gif')

    def recording_file_callback(self):
        self.file_callback_calls = {}
        def file_callback(context, key, fieldname, data, filename, mimetype, jsondata):
            self.file_callback_calls[fieldname] = dict(
                context=context,
                key=key,
                fieldname=fieldname,
                data=data,
                filename=filename,
                mimetype=mimetype)
        return file_callback

    def assert_file_callback(self, **assertions):
        self.assertIn('fieldname', assertions,
                      'assert_file_callback requires a "fieldname" keyword argument.')
        fieldname = assertions['fieldname']
        self.assertIn(fieldname, self.file_callback_calls,
                      'file_callback was not called for field "{0}"'.format(fieldname))

        data = self.file_callback_calls[fieldname]
        self.assertDictContainsSubset(assertions, data)
