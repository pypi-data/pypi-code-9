""" Tests for go_cli.main. """

from unittest import TestCase

from click.testing import CliRunner

from go_cli.main import cli


class TestCli(TestCase):
    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue("Vumi Go command line utility." in result.output)
        self.assertTrue("send  Send messages via an HTTP API (nostream)..."
                        in result.output)

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue("go-cli, version " in result.output)
