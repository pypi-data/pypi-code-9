""" Tests for go_cli.send. """

from unittest import TestCase
from StringIO import StringIO
import json
import types

import click
from click.testing import CliRunner

import go_cli.send
from go_cli.main import cli
from go_cli.send import messages_from_csv, messages_from_json
from go_cli.tests.utils import ApiHelper


class TestSendCommand(TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.api_helper = ApiHelper(self)
        self.api_helper.patch_api(go_cli.send, 'HttpApiSender')

    def tearDown(self):
        self.api_helper.tearDown()

    def invoke_send(self, args, account="acc-1", conv_key="conv-1",
                    conv_token="tok-1"):
        return self.runner.invoke(cli, [
            '--account', account, 'send',
            '--conversation', conv_key,
            '--token', conv_token,
        ] + args)

    def test_send_help(self):
        result = self.runner.invoke(cli, ['send', '--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(
            "Send messages via an HTTP API (nostream) conversation."
            in result.output)

    def test_send_no_conversation_details(self):
        result = self.runner.invoke(cli, ['send'])
        self.assertEqual(result.exit_code, 2)
        self.assertTrue(
            "Please specify all of the account key, conversation key and"
            " conversation authentication token. See --help."
            in result.output)

    def test_send_no_data(self):
        result = self.invoke_send([])
        self.assertEqual(result.exit_code, 2)
        self.assertTrue("Please specify either --csv or --json."
                        in result.output)

    def test_send_csv(self):
        response = self.api_helper.add_send("acc-1", "conv-1", "tok-1")
        with self.runner.isolated_filesystem():
            with open('msgs.csv', 'wb') as f:
                f.write("to_addr,content\n")
                f.write("+1234,hello\n")
            result = self.invoke_send(['--csv', 'msgs.csv'])
            self.assertEqual(result.output, "Sending message to +1234.\n")
            self.api_helper.check_response(
                response, 'PUT',
                {u'content': u'hello', u'to_addr': u'+1234'})

    def test_send_json(self):
        response = self.api_helper.add_send("acc-1", "conv-1", "tok-1")
        with self.runner.isolated_filesystem():
            with open('msgs.json', 'wb') as f:
                f.write(json.dumps({"to_addr": "+1234", "content": "hello"}))
                f.write("\n")
            result = self.invoke_send(['--json', 'msgs.json'])
            self.assertEqual(result.output, "Sending message to +1234.\n")
            self.api_helper.check_response(
                response, 'PUT',
                {u'content': u'hello', u'to_addr': u'+1234'})


class TestMessagesFromCsv(TestCase):
    def test_with_session_event(self):
        csv_file = StringIO("\n".join([
            "to_addr,content,session_event",
            "+1234,hello world,resume"
        ]))
        msgs = messages_from_csv(csv_file)
        self.assertTrue(isinstance(msgs, types.GeneratorType))
        self.assertEqual(list(msgs), [{
            'to_addr': '+1234', 'content': 'hello world',
            'session_event': 'resume',
        }])

    def test_without_session_event(self):
        csv_file = StringIO("\n".join([
            "to_addr,content",
            "+1234,hello world"
        ]))
        msgs = messages_from_csv(csv_file)
        self.assertTrue(isinstance(msgs, types.GeneratorType))
        self.assertEqual(list(msgs), [{
            'to_addr': '+1234', 'content': 'hello world',
            'session_event': None,
        }])

    def test_trailing_newline(self):
        csv_file = StringIO("\n".join([
            "to_addr,content",
            "+1234,hello world"
        ]) + "\n")
        msgs = messages_from_csv(csv_file)
        self.assertTrue(isinstance(msgs, types.GeneratorType))
        self.assertEqual(list(msgs), [{
            'to_addr': '+1234', 'content': 'hello world',
            'session_event': None,
        }])

    def test_invalid_headers(self):
        csv_file = StringIO("\n".join([
            "knights,niiii",
            "+1234,hello world"
        ]))
        msgs = messages_from_csv(csv_file)
        self.assertTrue(isinstance(msgs, types.GeneratorType))
        try:
            list(msgs)
        except click.UsageError as err:
            self.failUnlessEqual(
                str(err),
                "CSV file must contain to_addr and content column headers.")
        else:
            self.fail("Expected click.UsageError")


class TestMessagesFromJson(TestCase):
    def test_with_session_event(self):
        rows = [
            {"to_addr": "+1234", "content": "hello", "session_event": "new"},
            {"to_addr": "+1235", "content": "bye", "session_event": "close"},
        ]
        json_file = StringIO("\n".join(json.dumps(r) for r in rows))
        msgs = messages_from_json(json_file)
        self.assertTrue(isinstance(msgs, types.GeneratorType))
        self.assertEqual(list(msgs), rows)

    def test_without_session_event(self):
        rows = [
            {"to_addr": "+1234", "content": "hello"},
            {"to_addr": "+1235", "content": "bye"},
        ]
        json_file = StringIO("\n".join(json.dumps(r) for r in rows))
        msgs = messages_from_json(json_file)
        self.assertTrue(isinstance(msgs, types.GeneratorType))
        self.assertEqual(list(msgs), [
            dict(session_event=None, **r) for r in rows
        ])

    def test_trailing_newline(self):
        rows = [
            {"to_addr": "+1234", "content": "hello", "session_event": "new"},
            {"to_addr": "+1235", "content": "bye", "session_event": "close"},
        ]
        json_file = StringIO("\n".join(json.dumps(r) for r in rows) + "\n")
        msgs = messages_from_json(json_file)
        self.assertTrue(isinstance(msgs, types.GeneratorType))
        self.assertEqual(list(msgs), rows)

    def test_invalid_keys(self):
        rows = [
            {"to_addr": "+1234", "content": "hello", "session_event": "new"},
            {"knights": "+1235", "niiii": "bye", "session_event": "close"},
        ]
        json_file = StringIO("\n".join(json.dumps(r) for r in rows) + "\n")
        msgs = messages_from_json(json_file)
        self.assertTrue(isinstance(msgs, types.GeneratorType))
        try:
            list(msgs)
        except click.UsageError as err:
            self.failUnlessEqual(
                str(err),
                "JSON file lines must be objects containing to_addr and"
                " content keys.")
        else:
            self.fail("Expected click.UsageError")
