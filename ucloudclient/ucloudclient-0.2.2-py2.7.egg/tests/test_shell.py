__author__ = 'hyphen'
import re
import sys

import mock
from testtools import TestCase
from testtools import matchers
import fixtures
import six

from ucloudclient import uexceptions
import ucloudclient.shell


FAKE_ENV = {'UCLOUD_REGION': "cn-north-03",
            'UCLOUD_URL': "https://api.ucloud.cn",
            'UCLOUD_PUBKEY': "asdf",
            'UCLOUD_PRIKEY': "asdf"}

FAKE_ENV2 = {'UCLOUD_REGION': "cn-north-03",
             'UCLOUD_URL': "https://api.ucloud.cn",
             'UCLOUD_PUBKEY': "asdf",
             'UCLOUD_PRIKEY': "asdf"}


class ParserTest(TestCase):
    def setUp(self):
        super(ParserTest, self).setUp()
        self.parser = ucloudclient.shell.UcloudClientArgumentParser()

    def test_ambiguous_option(self):
        self.parser.add_argument('--tic')
        self.parser.add_argument('--tac')

        try:
            self.parser.parse_args(['--t'])
        except SystemExit as err:
            self.assertEqual(2, err.code)
        else:
            self.fail('SystemExit not raised')

    def test_not_really_ambiguous_option(self):
        # current/deprecated forms of the same option
        self.parser.add_argument('--tic-tac', action="store_true")
        self.parser.add_argument('--tic_tac', action="store_true")
        args = self.parser.parse_args(['--tic'])
        self.assertTrue(args.tic_tac)


class ShellTest(TestCase):
    _msg_no_region = ("You must provide region name via --ucloud_region "
                      "or env[UCLOUD_REGION].")
    _msg_no_url = ("You must provide url via --ucloud_url "
                   "or env[UCLOUD_URL].")
    _msg_no_public_key = ("You must provide public key via --ucloud_pubkey "
                          "or env[UCLOUD_PUBKEY].")
    _msg_no_private_key = ("You must provide private key via --ucloud_prikey "
                           "or env[UCLOUD_PRIKEY].")
    _msg_help = [
        '.*?^usage: ucloud',
        '.*?^\s+uhost-image-show\s+show image details',
        '.*?^See "ucloud help COMMAND" for help on a specific command.',
    ]

    def make_env(self, exclude=None, fake_env=FAKE_ENV):
        env = dict((k, v) for k, v in fake_env.items() if k != exclude)
        self.useFixture(fixtures.MonkeyPatch('os.environ', env))

    def setUp(self):
        super(ShellTest, self).setUp()
        self.useFixture(fixtures.MonkeyPatch(
            'ucloudclient.client.get_client_class',
            mock.MagicMock))

    def shell(self, argstr, exitcodes=(0,)):
        orig = sys.stdout
        orig_stderr = sys.stderr
        try:
            sys.stdout = six.StringIO()
            sys.stderr = six.StringIO()
            _shell = ucloudclient.shell.UcloudShell()
            _shell.main(argstr.split())
        except SystemExit:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.assertIn(exc_value.code, exitcodes)
        finally:
            stdout = sys.stdout.getvalue()
            sys.stdout.close()
            sys.stdout = orig
            stderr = sys.stderr.getvalue()
            sys.stderr.close()
            sys.stderr = orig_stderr
        return (stdout, stderr)

    def test_help_unknown_command(self):
        self.assertRaises(uexceptions.CommandError, self.shell, 'help foofoo')

    def test_help(self):
        required = self._msg_help
        stdout, stderr = self.shell('help')
        for r in required:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, re.DOTALL | re.MULTILINE))

    def test_help_on_subcommand(self):
        required = [
            '.*?^usage: ucloud uhost-image-show',
            '.*?^show image details',
            '.*?^Positional arguments:',
        ]
        stdout, stderr = self.shell('help uhost-image-show')
        for r in required:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, re.DOTALL | re.MULTILINE))

    def test_help_no_options(self):
        required = self._msg_help
        stdout, stderr = self.shell('')
        for r in required:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, re.DOTALL | re.MULTILINE))

    def test_bash_completion(self):
        stdout, stderr = self.shell('bash-completion')
        # just check we have some output
        required = [
            '.*uhost-reset-password',
            '.*--ostype',
            '.*help',
            '.*unet-sec-delete',
            '.*--chargetype']
        for r in required:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, re.DOTALL | re.MULTILINE))

    def test_no_region(self):
        required = self._msg_no_region
        self.make_env(exclude='UCLOUD_REGION')
        try:
            self.shell('uhost-list')
        except uexceptions.CommandError as message:
            self.assertEqual(required, message.args[0])
        else:
            self.fail('CommandError not raised')

    def test_no_url(self):
        required = self._msg_no_url
        self.make_env(exclude='UCLOUD_URL', fake_env=FAKE_ENV2)
        try:
            self.shell('uhost-list')
        except uexceptions.CommandError as message:
            self.assertEqual(required, message.args[0])
        else:
            self.fail('CommandError not raised')

    def test_no_public_key(self):
        required = self._msg_no_public_key
        self.make_env(exclude='UCLOUD_PUBKEY')
        try:
            self.shell('uhost-list')
        except uexceptions.CommandError as message:
            self.assertEqual(required, message.args[0])
        else:
            self.fail('CommandError not raised')

    def test_no_private_key(self):
        required = self._msg_no_private_key
        self.make_env(exclude='UCLOUD_PRIKEY', fake_env=FAKE_ENV2)
        try:
            self.shell('uhost-list')
        except uexceptions.CommandError as message:
            self.assertEqual(required, message.args[0])
        else:
            self.fail('CommandError not raised')
