# Tests for local ulif.openoffice processors.
import os
import shutil
import tempfile
import unittest
from ulif.openoffice.client import Client
from ulif.openoffice.helpers import get_entry_points
from psj.policy.transforms.cmd_oooconv import OPTIONS_HTML
from psj.policy.transforms.processors import PSJHTMLProcessor


class PSJHTMLProcessorTests(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.in_path = os.path.join(self.workdir, 'sample.html')
        self.doc_path = os.path.join(self.workdir, 'sample.doc')
        input_dir = os.path.join(os.path.dirname(__file__), 'input')
        self.doc_simple1_path = os.path.join(input_dir, 'simpledoc1.doc')
        self.css_sample_path = os.path.join(input_dir, 'sample.css')
        self.css_sample = open(self.css_sample_path, 'r').read()
        shutil.copy(self.doc_simple1_path, self.doc_path)
        self.result_path = None

    def tearDown(self):
        if os.path.exists(self.workdir):
            shutil.rmtree(self.workdir)
        if self.result_path and os.path.exists(self.result_path):
            shutil.rmtree(os.path.dirname(self.result_path))

    @property
    def transform_options(self):
        # OPTIONS_HTML with 'psj_html' stripped from 'meta-procord'
        options = dict(OPTIONS_HTML)
        options['meta-procord'] = options['meta-procord'].replace(
            'psj_html', '')
        return options

    def create_source(self):
        # create an additional CSS file for use with the in_path HTML
        client = Client()
        self.result_path, cache_key, metadata = client.convert(
            self.doc_path, self.transform_options)
        assert self.result_path is not None

    def test_registered(self):
        # make sure the processor is registered on startup
        assert 'psj_html' in get_entry_points('ulif.openoffice.processors')

    def test_args(self):
        # currently, we have no args to process
        proc = PSJHTMLProcessor()
        assert proc.args == []

    def test_process(self):
        # we can process docs. The result will be a doc with a <div> tag
        # accompanied by a CSS file called ``psj.css``.
        self.create_source()
        orig_path = self.result_path
        proc = PSJHTMLProcessor()
        self.result_path, metadata = proc.process(
            orig_path, {'error': False, 'error-descr': ''})
        assert metadata == {'error': False, 'error-descr': ''}
        assert not os.path.exists(orig_path)
        assert self.result_path != orig_path
        assert open(self.result_path, 'r').read().startswith('<div')
        dirlist = os.listdir(os.path.dirname(self.result_path))
        self.assertEqual(sorted(dirlist), ['psj.css', 'sample.html'])

    def test_process_invalid_ext(self):
        # we require a valid filename extension for source path
        proc = PSJHTMLProcessor()
        path, metadata = proc.process(
            '/some/filepath/with/invalid_ext.ext', "Fake-Metadata")
        assert path == '/some/filepath/with/invalid_ext.ext'
        assert metadata == "Fake-Metadata"

    def test_get_css(self):
        # we can get css files placed in result.
        for name in ['foo.html', 'foo.css', 'bar.css', 'baz.css']:
            open(os.path.join(self.workdir, name), 'w').write(
                'p {name="%s"}\n' % name)
        proc = PSJHTMLProcessor()
        result = proc.get_css(self.workdir)
        self.assertEqual(
            result, ('p {name="bar.css"}\np {name="baz.css"}\n'
                     'p {name="foo.css"}\n'))
        # non-css files remain
        assert os.path.exists(os.path.join(self.workdir, 'foo.html'))
        # css files are removed
        assert not os.path.exists(os.path.join(self.workdir, 'foo.css'))
        assert not os.path.exists(os.path.join(self.workdir, 'bar.css'))
        assert not os.path.exists(os.path.join(self.workdir, 'baz.css'))

    def test_fix_css(self):
        # we can 'fix' code in CSS
        proc = PSJHTMLProcessor()
        self.assertEqual(  # empty CSS
            proc.fix_css(''), '')
        self.assertEqual(  # base CSS
            proc.fix_css('p {color:#000;}'),
            '#psj-doc p{color:#000}')
        self.assertEqual(  # CSS with OR selector (,)
            proc.fix_css('div, p {color:#000;}'),
            '#psj-doc div,#psj-doc p{color:#000}')
        self.assertEqual(  # CSS with linebreaks
            proc.fix_css('p {color:#000;}\ndiv#num1 {color: #fff}'),
            '#psj-doc p{color:#000}#psj-doc div#num1{color:#fff}')
        self.assertEqual(  # 'body' selector replaced
            proc.fix_css('body {color:#000;}'),
            '#psj-doc{color:#000}')

    def test_fix_html(self):
        # we can 'fix' HTML docs
        code = ("<html><head><title>t</title></head>"
                "<body><h1>head</h1></body></html>")
        proc = PSJHTMLProcessor()
        self.assertEqual(
            proc.fix_html(code),
            '<div id="psj-doc"><h1>head</h1></div>\n'
            )

    def test_proc_always_generates_css(self):
        # make sure we alway get a CSS file called 'psj.css',
        # even if no CSS was put in.
        proc = PSJHTMLProcessor()
        dir_path = tempfile.mkdtemp()
        html_path = os.path.join(dir_path, 'sample.html')
        with open(html_path, 'wb') as fd:
            fd.write('<html><body><h1>Foo</h1></body></html>')
        self.result_path, metadata = proc.process(
            html_path, {'error': False, 'error-descr': ''})
        result_dir = os.path.dirname(self.result_path)
        assert sorted(os.listdir(result_dir)) == ['psj.css', 'sample.html']
        with open(os.path.join(result_dir, 'psj.css'), 'rb') as fd:
            css = fd.read()
        assert css == ''
