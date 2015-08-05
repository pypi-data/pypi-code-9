import codecs
from collections import OrderedDict
import tempfile
from mock import patch

from okapi.settings import settings
from okapi.runners import Runner
from okapi.tests.utils import TestCase
from okapi.core.request import DummyResponse


class RunnerTest(TestCase):
    @staticmethod
    def __rst(s):
        f = tempfile.TemporaryFile()
        f.write(codecs.encode(s, 'utf-8'))
        f.seek(0)
        return f

    def test_save_output(self):
        output = tempfile.TemporaryDirectory()
        f = self.__rst('*OK*')
        runner = Runner(f.name, 'http://example.foo')
        runner.render()
        runner.save(output.name)
        self.assertIn('<em>OK</em>', open(output.name + '/index.html').read())

    # region Test creating requests
    @patch('requests.request')
    def test_request_ok(self, request):
        request.return_value = DummyResponse(status_code=200)

        f = self.__rst(
            '.. code:: request\n'
            '    \n'
            '    GET /api/test/ok/\n'
            '    \n'
            '    > status_code == 200\n'
            '    \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        runner.render()

        self.assertIn('[OK] status_code == 200', settings.log.buffer[0])
        request.assert_called_with(
            'get', 'http://example.foo/api/test/ok/',
            headers=OrderedDict(), data=''
        )

    @patch('requests.request')
    def test_request_fail(self, request):
        request.return_value = DummyResponse(status_code=404)

        f = self.__rst(
            '.. code:: request\n'
            '    \n'
            '    GET /api/test/ok/\n'
            '    \n'
            '    > status_code == 200\n'
            '    \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        runner.render()

        self.assertIn('[FAIL] status_code == 200', settings.log.buffer[0])
        request.assert_called_with(
            'get', 'http://example.foo/api/test/ok/',
            headers=OrderedDict(), data=''
        )

    @patch('requests.request')
    def test_request_without_tests(self, request):
        request.return_value = DummyResponse(status_code=404)

        f = self.__rst(
            '.. code:: request\n'
            '    \n'
            '    GET /api/test/ok/\n'
            '    \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        runner.render()

        self.assertIn('[WARN] Request has no tests', settings.log.buffer[0])
        request.assert_called_with(
            'get', 'http://example.foo/api/test/ok/',
            headers=OrderedDict(), data=''
        )

    @patch('requests.request')
    def test_request_with_headers(self, request):
        request.return_value = DummyResponse(status_code=201)

        f = self.__rst(
            '.. code:: request\n'
            '   \n'
            '   POST /api/test/ok/\n'
            '   Accept-Language: en,fr\n'
            '   Cookies: foo\n'
            '   \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        runner.render()

        request.assert_called_with(
            'post', 'http://example.foo/api/test/ok/',
            headers=OrderedDict([
                ('Accept-Language', 'en,fr'),
                ('Cookies', 'foo')
            ]),
            data=''
        )

    @patch('requests.request')
    def test_request_with_json_payload(self, request):
        request.return_value = DummyResponse(status_code=201)

        f = self.__rst(
            '.. code:: request\n'
            '   \n'
            '   POST /api/test/ok/\n'
            '   \n'
            '   {"foo": "bar"}\n'
            '   \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        rendered = runner.render()

        request.assert_called_with(
            'post', 'http://example.foo/api/test/ok/',
            headers=OrderedDict(),
            data='{"foo": "bar"}'
        )
        self.assertIn('{&#34;foo&#34;:\xa0&#34;bar&#34;}', rendered)

    @patch('requests.request')
    def test_request_with_text_payload(self, request):
        request.return_value = DummyResponse(status_code=201)

        f = self.__rst(
            '.. code:: request\n'
            '   \n'
            '   POST /api/test/ok/\n'
            '   \n'
            '   OK\n'
            '   \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        runner.render()

        request.assert_called_with(
            'post', 'http://example.foo/api/test/ok/',
            headers=OrderedDict(),
            data='OK'
        )

    @patch('requests.request')
    def test_request_post(self, request):
        request.return_value = DummyResponse(status_code=204)

        f = self.__rst(
            '.. code:: request\n'
            '   \n'
            '   POST /api/test/ok/\n'
            '   \n'
            '   > status_code == 204\n'
            '   \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        print(runner.render())

        self.assertIn('post /api/test/ok/', settings.log.buffer[0])
        request.assert_called_with(
            'post', 'http://example.foo/api/test/ok/',
            headers=OrderedDict(), data=''
        )

    def test_request_bad_method(self):
        f = self.__rst(
            '.. code:: request\n'
            '   \n'
            '   PO /api/test/ok/\n'
            '   \n'
            '   > status_code == 204\n'
            '   \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        runner.render()

        self.assertIn(
            'Could not parse request line `PO /api/test/ok/`',
            settings.log.buffer
        )

    @patch('requests.request')
    def test_escape_html_in_request(self, request):
        request.return_value = DummyResponse(status_code=200)

        f = self.__rst(
            '.. code:: request\n'
            '   \n'
            '   GET /api/test/ok/\n'
            '   \n'
            '   <strong>FOO</strong>'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        rendered = runner.render()

        self.assertIn('&lt;strong&gt;FOO&lt;/strong&gt;', rendered)

    # endregion

    # region Test getting responses
    @patch('requests.request')
    def test_response_json(self, request):
        request.return_value = DummyResponse(content='{"foo": "bar"}')

        f = self.__rst(
            '.. code:: request\n'
            '    \n'
            '    GET /api/test/ok/\n'
            '    \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        rendered = runner.render()

        expected_output = \
            '{<br>\n\xa0\xa0&#34;foo&#34;:\xa0&#34;bar&#34;<br>\n}'
        self.assertIn(expected_output, rendered)

    @patch('requests.request')
    def test_response_text(self, request):
        request.return_value = DummyResponse(content='FOOBAR')

        f = self.__rst(
            '.. code:: request\n'
            '    \n'
            '    GET /api/test/ok/\n'
            '    \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        rendered = runner.render()

        self.assertIn('FOOBAR', rendered)

    @patch('requests.request')
    def test_escape_html_in_response(self, request):
        request.return_value = DummyResponse(content='<strong>FOO</strong>')

        f = self.__rst(
            '.. code:: request\n'
            '    \n'
            '    GET /api/test/ok/\n'
            '    \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        rendered = runner.render()

        self.assertIn('&lt;strong&gt;FOO&lt;/strong&gt;', rendered)

    # endregion

    # region Test headers
    def test_headers_directive_usage(self):
        f = self.__rst(
            '.. code:: headers\n'
            '    \n'
            '    Accept-Language: en,fr\n'
            '    Accept-Type: application/json\n'
            '    \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        runner.render()

        self.assertEqual(settings.headers.visible, {
            'Accept-Language': 'en,fr',
            'Accept-Type': 'application/json'
        })

    def test_badly_formatted_headers(self):
        f = self.__rst(
            '.. code:: headers\n'
            '    \n'
            '    Accept-Language en,fr\n'
            '    Accept-Type: application/json\n'
            '    \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        runner.render()

        self.assertIn(
            'Cannot parse headers line `Accept-Language en,fr`',
            settings.log.buffer
        )

    @patch('requests.request')
    def test_hidden_headers_are_not_in_html(self, request):
        request.return_value = DummyResponse()
        settings.hidden = {'Authorization': 'topsecrettoken'}

        f = self.__rst(
            '.. code:: request\n'
            '    \n'
            '    GET /api/test/\n'
            '    \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        rendered = runner.render()
        self.assertNotIn('topsecrettoken', rendered)

    @patch('requests.request')
    def test_hidden_headers_overwrite_other_headers(self, request):
        request.return_value = DummyResponse()
        settings.headers.hidden = {'Authorization': 'topsecrettoken'}

        f = self.__rst(
            '.. code:: request\n'
            '    \n'
            '    GET /api/test/\n'
            '    Authorization: TOKEN'
            '    \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        rendered = runner.render()
        self.assertIn('Authorization: TOKEN', rendered)

        request.assert_called_with(
            'get', 'http://example.foo/api/test/',
            headers=OrderedDict([
                ('Authorization', 'topsecrettoken')
            ]),
            data=''
        )

    @patch('requests.request')
    def test_local_headers_overwrite_visible_headers(self, request):
        request.return_value = DummyResponse()

        f = self.__rst(
            '.. code:: headers\n'
            '   \n'
            '   Credentials: user:password\n'
            '   \n'
            '.. code:: request\n'
            '    \n'
            '    GET /api/test/\n'
            '    Credentials: foo:bar'
            '    \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        runner.render()

        request.assert_called_with(
            'get', 'http://example.foo/api/test/',
            headers=OrderedDict([
                ('Credentials', 'foo:bar')
            ]),
            data=''
        )
    # endregion

    @patch('requests.request')
    def test_curl_export(self, request):
        request.return_value = DummyResponse()
        f = self.__rst(
            '.. code:: headers\n'
            '   \n'
            '   Authorization: topsecrettoken\n'
            '   \n'
            '\n'
            '.. code:: request\n'
            '   \n'
            '   POST /api/test/\n'
            '   Credentials: foo:bar'
            '   \n'
            '   {\n'
            '       "foo": "bar"\n'
            '   }\n'
            '   \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        rendered = runner.render()

        self.assertIn('curl --include', rendered)
        self.assertIn('--request POST', rendered)
        self.assertIn('--header "Authorization: topsecrettoken"', rendered)
        self.assertIn('--header "Credentials: foo:bar"', rendered)
        self.assertIn('--data-binary "{    \\"foo\\": \\"bar\\"}"', rendered)
        self.assertIn('"http://example.foo/api/test/"', rendered)

    @patch('requests.request')
    def test_breadcrumbs(self, request):
        request.return_value = DummyResponse()

        f = self.__rst(
            'Top header\n'
            '==========\n'
            '\n'
            'Second header\n'
            '-------------\n '
            '\n'
            'Third header\n'
            '************\n'
            '\n'
            '.. code:: request\n'
            '    \n'
            '    GET /api/test/\n'
            '    \n'
        )

        runner = Runner(f.name, 'http://example.foo')
        runner.render()

        self.assertIn(
            'TOP HEADER > SECOND HEADER > THIRD HEADER',
            settings.log.buffer[0]
        )

    def test_simple_code_block_should_still_work(self):
        f = self.__rst(
            'Test: \n'
            '\n'
            '.. code:: html\n'
            '   \n'
            '   <strong>OK<-strong>\n'
            '   \n'
            '\n'
        )

        runner = Runner(f.name, 'http://example.foo')
        rendered = runner.render()
        self.assertIn('<pre class="code html literal-block">', rendered)

    @patch('requests.request')
    def test_described_url(self, request):
        request.return_value = DummyResponse()

        f = self.__rst(
            '.. code:: request\n'
            '   \n'
            '   GET /api/test/{userId:1}/{threadId:5}/\n'
            '   \n'
            ''
        )

        runner = Runner(f.name, 'http://example.foo')
        rendered = runner.render()
        self.assertIn(
            '/api/test/'
            '<abbr data-toggle="tooltip" data-placement="top" '
            'title="userId">1</abbr>/'
            '<abbr data-toggle="tooltip" data-placement="top" '
            'title="threadId">5</abbr>/',
            rendered
        )
