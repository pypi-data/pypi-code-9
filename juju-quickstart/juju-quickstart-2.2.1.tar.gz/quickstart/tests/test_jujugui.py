# This file is part of the Juju Quickstart Plugin, which lets users set up a
# Juju environment in very few steps (https://launchpad.net/juju-quickstart).
# Copyright (C) 2015 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License version 3, as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for the Quickstart Juju GUI charm and service helpers."""

from __future__ import unicode_literals

import unittest

from jujubundlelib import references
import mock

from quickstart import jujugui
from quickstart.tests import helpers


class TestAddTokensToUrl(unittest.TestCase):

    def test_tokens(self):
        # The URL is properly generated with both authentication and changes
        # tokens.
        url = jujugui.add_tokens_to_url(
            'https://1.2.3.4', 'myauth', 'mychanges')
        self.assertEqual(
            'https://1.2.3.4/?authtoken=myauth&changestoken=mychanges', url)

    def test_auth_token_only(self):
        # The URL is properly generated with the authentication token only.
        url = jujugui.add_tokens_to_url('https://1.2.3.4', 'login', None)
        self.assertEqual('https://1.2.3.4/?authtoken=login', url)

    def test_changes_token_only(self):
        # The URL is properly generated with the changes token only.
        url = jujugui.add_tokens_to_url('https://1.2.3.4', None, 'changeset')
        self.assertEqual('https://1.2.3.4/?changestoken=changeset', url)

    def test_no_tokens(self):
        # The URL is left untouched if no tokens are provided.
        url = 'http://example.com'
        self.assertEqual(url, jujugui.add_tokens_to_url(url, None, None))


class TestBuildOptions(unittest.TestCase):

    def test_no_options(self):
        # None is returned if there are no customized options.
        options = jujugui.build_options(None, None)
        self.assertIsNone(options)

    def test_port(self):
        # The port option is correctly configured.
        options = jujugui.build_options(42, None)
        self.assertEqual({'port': 42}, options)

    def test_gui_source(self):
        # The GUI source option is correctly configured.
        options = jujugui.build_options(None, ('who', 'develop'))
        expected_options = {
            'juju-gui-source': 'https://github.com/who/juju-gui.git develop',
        }
        self.assertEqual(expected_options, options)

    def test_all_options(self):
        # Multiple options are properly configured.
        options = jujugui.build_options(443, ('juju', 'beta'))
        expected_options = {
            'juju-gui-source': 'https://github.com/juju/juju-gui.git beta',
            'port': 443,
        }
        self.assertEqual(expected_options, options)


class TestIsPromulgated(unittest.TestCase):

    def test_promulgated(self):
        # Promulgated Juju GUI charm references are properly recognized.
        for url in ('cs:precise/juju-gui-0', 'cs:trusty/juju-gui-42'):
            ref = references.Reference.from_string(url)
            self.assertTrue(jujugui.is_promulgated(ref), url)

    def test_customized(self):
        # Customized Juju GUI charm references are properly recognized.
        tests = (
            'local:precise/juju-gui-0',
            'cs:precise/mygui-1',
            'cs:~who/trusty/juju-gui-2',
        )
        for url in tests:
            ref = references.Reference.from_string(url)
            self.assertFalse(jujugui.is_promulgated(ref), url)


class TestNormalizeConfig(unittest.TestCase):

    def test_normal_options(self):
        # The options are not modified if there is no need.
        original_options = {'port': 8080, 'secure': True}
        options = jujugui.normalize_config(original_options)
        self.assertEqual(original_options, options)

    def test_port(self):
        # A default port is set if it is not present in the input options.
        options = jujugui.normalize_config({'port': None, 'secure': True})
        self.assertEqual({'port': 443, 'secure': True}, options)

    def test_not_modified_in_place(self):
        # The input options are not modified in place.
        original_options = {'port': None, 'sandbox': False, 'secure': True}
        options = jujugui.normalize_config(original_options)
        options['sandbox'] = True
        self.assertEqual(
            {'port': 443, 'sandbox': True, 'secure': True}, options)
        self.assertEqual(
            {'port': None, 'sandbox': False, 'secure': True}, original_options)

    def test_secure_warning(self):
        # A warning is logged if the GUI service is running in insecure mode.
        expected_log = 'the Juju GUI is running in insecure mode'
        with helpers.assert_logs([expected_log], level='warn'):
            jujugui.normalize_config({'port': 8080, 'secure': False})


@mock.patch('__builtin__.print', mock.Mock())
class TestParseGuiCharmUrl(unittest.TestCase):

    def test_charm_instance_returned(self):
        # A charm reference instance is correctly returned.
        ref = jujugui.parse_charm_url('cs:trusty/juju-gui-42')
        self.assertIsInstance(ref, references.Reference)
        self.assertEqual('cs:trusty/juju-gui-42', ref.id())

    def test_customized(self):
        # A customized charm reference is properly logged.
        expected = 'using a customized juju-gui charm'
        with helpers.assert_logs([expected], level='warn'):
            jujugui.parse_charm_url('cs:~juju-gui/precise/juju-gui-28')

    def test_outdated(self):
        # An outdated charm reference is properly logged.
        expected = 'charm is outdated and may not support bundle deployments'
        with helpers.assert_logs([expected], level='warn'):
            jujugui.parse_charm_url('cs:precise/juju-gui-1')

    def test_unexpected(self):
        # An unexpected charm reference is properly logged.
        expected = (
            'unexpected URL for the juju-gui charm: the service may not work '
            'as expected')
        with helpers.assert_logs([expected], level='warn'):
            jujugui.parse_charm_url('cs:precise/another-gui-42')

    def test_official(self):
        # No warnings are logged if an up to date charm is passed.
        with mock.patch('logging.warn') as mock_warn:
            jujugui.parse_charm_url('cs:precise/juju-gui-100')
        self.assertFalse(mock_warn.called)
