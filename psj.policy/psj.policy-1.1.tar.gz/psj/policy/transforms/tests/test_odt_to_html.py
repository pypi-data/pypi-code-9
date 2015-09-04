# Tests for the odt_to_html module
import os
import tempfile
import shutil
import unittest
from Products.PortalTransforms.interfaces import ITransform
from Products.PortalTransforms.data import datastream
from ulif.openoffice.cachemanager import CacheManager, get_marker
from zope.interface.verify import verifyObject, verifyClass
from psj.policy.testing import IntegrationTestCase
from psj.policy.transforms.cmd_oooconv import OPTIONS_HTML, OPTIONS_PDF
from psj.policy.transforms.odt_to_html import Odt2Html, register


class HelperTests(unittest.TestCase):
    # Tests for non-Odt2Html components in module

    def test_register(self):
        # there is a register function that returns an appropriate object
        assert isinstance(register(), Odt2Html)


class FakeContext(object):
    # a context that holds cache keys.
    def __init__(self, html_key=None, pdf_key=None):
        self.cache_key_html = html_key
        self.cache_key_pdf = pdf_key


class Odt2HtmlTests(unittest.TestCase):
    # Tests for Odt2Html class

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.inputdir = os.path.join(os.path.dirname(__file__), 'input')
        self.cachedir = tempfile.mkdtemp()
        self.src_path1 = os.path.join(self.workdir, 'sample1.odt')
        self.src_path2 = os.path.join(self.workdir, 'sample2.odt')
        shutil.copy2(
            os.path.join(self.inputdir, 'testdoc1.odt'), self.src_path1)
        shutil.copy2(
            os.path.join(self.inputdir, 'testdoc2.odt'), self.src_path2)

    def tearDown(self):
        shutil.rmtree(self.workdir)
        if os.path.isdir(self.cachedir):
            shutil.rmtree(self.cachedir)

    def register_fakedoc_in_cache(self, src, options):
        # register a fake doc in cache. Result cache_key is based on
        # path to src document and options given.
        cm = CacheManager(self.cachedir)
        fake_result_path = os.path.join(self.workdir, 'result.html')
        open(fake_result_path, 'w').write('A fake result.')
        marker = get_marker(options)
        cache_key = cm.register_doc(src, fake_result_path, repr_key=marker)
        return cache_key

    def test_iface(self):
        # make sure we fullfill interface contracts
        obj = Odt2Html()
        verifyClass(ITransform, Odt2Html)
        verifyObject(ITransform, obj)

    def test_mimetypes(self):
        # we have proper mimetypes set
        transform = Odt2Html()
        self.assertEqual(transform.output, 'text/html')
        self.assertEqual(transform.output_encoding, 'utf-8')
        self.assertEqual(transform.inputs,
                         ('application/vnd.oasis.opendocument.text',))

    def test_name(self):
        # we can get the transform name
        transform = Odt2Html()
        self.assertEqual(transform.name(), 'odt_to_html')
        self.assertEqual(transform.name('other_name'), 'odt_to_html')

    def test_cache_dir(self):
        # we can set/get a cache dir
        transform = Odt2Html(cache_dir='/foo')
        self.assertEqual(transform.cache_dir, '/foo')

    def test_cache_dir_default(self):
        # we have a cache_dir default (emtpy string)
        transform = Odt2Html()
        self.assertEqual(transform.cache_dir, '')

    def test_convert(self):
        # we can convert odt docs to HTML.
        transform = Odt2Html()
        idatastream = datastream('mystream')
        transform.convert(
            open(self.src_path2, 'r').read(),
            idatastream)
        assert '</span>' in idatastream.getData()
        self.assertEqual(idatastream.getMetadata(), {'cache_key_html': None})

    def test_convert_with_cachekey(self):
        # we retrieve cached files if cache_key is set and valid
        cache_key = self.register_fakedoc_in_cache(
            src=self.src_path1, options=OPTIONS_HTML)
        transform = Odt2Html(cache_dir=self.cachedir)
        idatastream = datastream('mystream')
        # set cache key for HTML
        idatastream.context = FakeContext(html_key=cache_key)
        transform.convert(
            # We give a different source than what was cached as source.
            # This way we can be sure that if we get the fake result, it was
            # really retrieved via cache key lookup and not via source
            # lookup.
            open(self.src_path2, 'r').read(),
            idatastream)
        assert idatastream.getData() == 'A fake result.'


class Odt2HtmlIntegrationTests(IntegrationTestCase):

    def test_registered(self):
        # the transform is registered in a standard plonesite after install
        transforms = self.portal.portal_transforms
        assert 'odt_to_html' in transforms.keys()
