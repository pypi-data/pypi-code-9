# Copyright 2013 Canonical Ltd.  This software is licensed under the
# GNU General Public License version 3 (see the file LICENSE).
from __future__ import absolute_import, unicode_literals
import json
import os
import tempfile
from collections import namedtuple
from unittest import TestCase, skip

from mock import ANY, DEFAULT, patch
from requests import Response

from click_toolbelt import __namespace__
from click_toolbelt.common import CommandError
from click_toolbelt.constants import (
    UBUNTU_SSO_API_ROOT_URL,
)
from click_toolbelt.upload import (
    Upload,
)
from click_toolbelt.tests.test_common import (
    CommandTestCase,
)


class UploadCommandBaseTestCase(CommandTestCase):
    command_class = Upload

    def setUp(self):
        super(UploadCommandBaseTestCase, self).setUp()

        # setup patches
        mock_environ = {
            'UBUNTU_SSO_API_ROOT_URL': UBUNTU_SSO_API_ROOT_URL,
        }
        patcher = patch('click_toolbelt.upload.os.environ', mock_environ)
        patcher.start()
        self.addCleanup(patcher.stop)

        name = 'click_toolbelt.upload.Upload.get_oauth_session'
        patcher = patch(name)
        self.mock_get_oauth_session = patcher.start()
        self.mock_get = self.mock_get_oauth_session.return_value.get
        self.mock_post = self.mock_get_oauth_session.return_value.post
        self.addCleanup(patcher.stop)


class UploadFilesTestCase(UploadCommandBaseTestCase):

    def setUp(self):
        super(UploadFilesTestCase, self).setUp()
        self.binary_file = self.get_temporary_file()

    def test_upload_files(self):
        mock_response = self.mock_post.return_value
        mock_response.ok = True
        mock_response.json.return_value = {
            'successful': True,
            'upload_id': 'some-valid-upload-id',
        }

        response = self.command.upload_files(self.binary_file.name)
        self.assertEqual(response, {
            'success': True,
            'errors': [],
            'upload_id': 'some-valid-upload-id',
            'binary_filesize': os.path.getsize(self.binary_file.name),
            'source_uploaded': False,
        })

    def test_upload_files_uses_environment_variables(self):
        with patch.dict(os.environ,
                        CLICK_UPDOWN_UPLOAD_URL='http://example.com'):
            upload_url = 'http://example.com/unscanned-upload/'
            self.command.upload_files(self.binary_file.name)
            self.mock_post.assert_called_once_with(
                upload_url, files={'binary': ANY})

    def test_upload_files_with_source_upload(self):
        mock_response = self.mock_post.return_value
        mock_response.ok = True
        mock_response.json.return_value = {
            'successful': True,
            'upload_id': 'some-valid-upload-id',
        }

        response = self.command.upload_files(self.binary_file.name)
        self.assertEqual(response, {
            'success': True,
            'errors': [],
            'upload_id': 'some-valid-upload-id',
            'binary_filesize': os.path.getsize(self.binary_file.name),
            'source_uploaded': False,
        })

    def test_upload_files_with_invalid_oauth_session(self):
        self.mock_get_oauth_session.return_value = None
        response = self.command.upload_files(self.binary_file.name)
        self.assertEqual(response, {
            'success': False,
            'errors': ['No valid credentials found.'],
        })
        self.assertFalse(self.mock_post.called)

    def test_upload_files_error_response(self):
        mock_response = self.mock_post.return_value
        mock_response.ok = False
        mock_response.reason = '500 INTERNAL SERVER ERROR'
        mock_response.text = 'server failed'

        response = self.command.upload_files(self.binary_file.name)
        self.assertEqual(response, {
            'success': False,
            'errors': ['server failed'],
        })

    def test_upload_files_handle_malformed_response(self):
        mock_response = self.mock_post.return_value
        mock_response.json.return_value = {'successful': False}

        response = self.command.upload_files(self.binary_file.name)
        err = KeyError('upload_id')
        self.assertEqual(response, {
            'success': False,
            'errors': [str(err)],
        })


class UploadAppTestCase(UploadCommandBaseTestCase):

    def setUp(self):
        super(UploadAppTestCase, self).setUp()
        self.data = {
            'upload_id': 'some-valid-upload-id',
            'binary_filesize': 123456,
            'source_uploaded': False,
        }
        self.package_name = 'namespace.binary'

        patcher = patch.multiple(
            'click_toolbelt.upload',
            SCAN_STATUS_POLL_DELAY=0.0001)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_upload_app_with_invalid_oauth_session(self):
        self.mock_get_oauth_session.return_value = None
        response = self.command.upload_app(self.package_name, self.data)
        self.assertEqual(response, {
            'success': False,
            'errors': ['No valid credentials found.'],
            'application_url': '',
        })

    def test_upload_app_uses_environment_variables(self):
        with patch.dict(os.environ,
                        MYAPPS_API_ROOT_URL='http://example.com'):
            upload_url = ("http://example.com/click-package-upload/%s/" %
                          self.package_name)
            data = {
                'updown_id': self.data['upload_id'],
                'binary_filesize': self.data['binary_filesize'],
                'source_uploaded': self.data['source_uploaded'],
            }
            self.command.upload_app(self.package_name, self.data)
            self.mock_post.assert_called_once_with(
                upload_url, data=data, files=[])

    def test_upload_app(self):
        mock_response = self.mock_post.return_value
        mock_response.ok = True
        mock_response.json.return_value = {
            'success': True,
            'status_url': 'http://example.com/status/'
        }

        mock_status_response = self.mock_get.return_value
        mock_status_response.ok = True
        mock_status_response.json.return_value = {
            'completed': True
        }

        response = self.command.upload_app(self.package_name, self.data)
        self.assertEqual(response, {
            'success': True,
            'errors': [],
            'application_url': '',
        })

    def test_upload_app_error_response(self):
        mock_response = self.mock_post.return_value
        mock_response.ok = False
        mock_response.reason = '500 INTERNAL SERVER ERROR'
        mock_response.text = 'server failure'

        response = self.command.upload_app(self.package_name, self.data)
        self.assertEqual(response, {
            'success': False,
            'errors': ['server failure'],
            'application_url': '',
        })

    def test_upload_app_handle_malformed_response(self):
        mock_response = self.mock_post.return_value
        mock_response.ok = True
        mock_response.json.return_value = {}

        response = self.command.upload_app(self.package_name, self.data)
        err = KeyError('status_url')
        self.assertEqual(response, {
            'success': False,
            'errors': [str(err)],
            'application_url': '',
        })

    def test_upload_app_with_errors_during_scan(self):
        mock_response = self.mock_post.return_value
        mock_response.ok = True
        mock_response.json.return_value = {
            'success': True,
            'status_url': 'http://example.com/status/'
        }

        mock_status_response = self.mock_get.return_value
        mock_status_response.ok = True
        mock_status_response.json.return_value = {
            'completed': True,
            'message': 'some error',
            'application_url': 'http://example.com/myapp',
        }

        response = self.command.upload_app(self.package_name, self.data)
        self.assertEqual(response, {
            'success': False,
            'errors': ['some error'],
            'application_url': 'http://example.com/myapp'
        })

    def test_upload_app_poll_status(self):
        mock_response = self.mock_post.return_value
        mock_response.ok = True
        mock_response.return_value = {
            'success': True,
            'status_url': 'http://example.com/status/'
        }

        response_not_completed = Response()
        response_not_completed.status_code = 200
        response_not_completed.encoding = 'utf-8'
        response_not_completed._content = json.dumps(
            {'completed': False, 'application_url': ''}).encode('utf-8')
        response_completed = Response()
        response_completed.status_code = 200
        response_completed.encoding = 'utf-8'
        response_completed._content = json.dumps(
            {'completed': True,
             'application_url': 'http://example.org'}).encode('utf-8')
        self.mock_get.side_effect = [
            response_not_completed,
            response_not_completed,
            response_completed,
        ]
        response = self.command.upload_app(self.package_name, self.data)
        self.assertEqual(response, {
            'success': True,
            'errors': [],
            'application_url': 'http://example.org',
        })
        self.assertEqual(self.mock_get.call_count, 3)

    def test_upload_app_ignore_non_ok_responses(self):
        mock_response = self.mock_post.return_value
        mock_response.ok = True
        mock_response.return_value = {
            'success': True,
            'status_url': 'http://example.com/status/',
        }

        ok_response = Response()
        ok_response.status_code = 200
        ok_response.encoding = 'utf-8'
        ok_response._content = json.dumps(
            {'completed': True}).encode('utf-8')
        nok_response = Response()
        nok_response.status_code = 503

        self.mock_get.side_effect = [nok_response, nok_response, ok_response]
        response = self.command.upload_app(self.package_name, self.data)
        self.assertEqual(response, {
            'success': True,
            'errors': [],
            'application_url': '',
        })
        self.assertEqual(self.mock_get.call_count, 3)

    def test_upload_app_abort_polling(self):
        mock_response = self.mock_post.return_value
        mock_response.ok = True
        mock_response.json.return_value = {
            'success': True,
            'status_url': 'http://example.com/status/',
            'web_status_url': 'http://example.com/status-web/',
        }

        mock_status_response = self.mock_get.return_value
        mock_status_response.ok = True
        mock_status_response.json.return_value = {
            'completed': False
        }
        response = self.command.upload_app(self.package_name, self.data)
        self.assertEqual(response, {
            'success': False,
            'errors': [
                'Package scan took too long.',
                'Please check the status later at: '
                'http://example.com/status-web/.',
            ],
            'application_url': '',
        })

    def test_upload_app_abort_polling_without_web_status_url(self):
        mock_response = self.mock_post.return_value
        mock_response.ok = True
        mock_response.json.return_value = {
            'success': True,
            'status_url': 'http://example.com/status/',
        }

        mock_status_response = self.mock_get.return_value
        mock_status_response.ok = True
        mock_status_response.json.return_value = {
            'completed': False
        }
        response = self.command.upload_app(self.package_name, self.data)
        self.assertEqual(response, {
            'success': False,
            'errors': [
                'Package scan took too long.',
            ],
            'application_url': '',
        })

    def test_upload_app_with_metadata(self):
        self.command.upload_app(self.package_name, self.data,
                                metadata={'changelog': 'some changes',
                                          'tagline': 'a tagline'})
        self.mock_post.assert_called_once_with(
            ANY,
            data={
                'updown_id': self.data['upload_id'],
                'binary_filesize': self.data['binary_filesize'],
                'source_uploaded': self.data['source_uploaded'],
                'changelog': 'some changes',
                'tagline': 'a tagline',
            },
            files=[],
        )

    def test_upload_app_ignore_special_attributes_in_metadata(self):
        self.command.upload_app(
            self.package_name,
            self.data, metadata={
                'changelog': 'some changes',
                'tagline': 'a tagline',
                'upload_id': 'my-own-id',
                'binary_filesize': 0,
                'source_uploaded': False,
            })
        self.mock_post.assert_called_once_with(
            ANY,
            data={
                'updown_id': self.data['upload_id'],
                'binary_filesize': self.data['binary_filesize'],
                'source_uploaded': self.data['source_uploaded'],
                'changelog': 'some changes',
                'tagline': 'a tagline',
            },
            files=[],
        )

    @patch('click_toolbelt.upload.open')
    def test_upload_app_with_icon(self, mock_open):
        with tempfile.NamedTemporaryFile() as icon:
            mock_open.return_value = icon

            self.command.upload_app(
                self.package_name, self.data,
                metadata={
                    'icon_256': icon.name,
                }
            )
            self.mock_post.assert_called_once_with(
                ANY,
                data={
                    'updown_id': self.data['upload_id'],
                    'binary_filesize': self.data['binary_filesize'],
                    'source_uploaded': self.data['source_uploaded'],
                },
                files=[
                    ('icon_256', icon),
                ],
            )

    @patch('click_toolbelt.upload.open')
    def test_upload_app_with_screenshots(self, mock_open):
        screenshot1 = tempfile.NamedTemporaryFile()
        screenshot2 = tempfile.NamedTemporaryFile()
        mock_open.side_effect = [screenshot1, screenshot2]

        self.command.upload_app(
            self.package_name, self.data,
            metadata={
                'screenshots': [screenshot1.name, screenshot2.name],
            }
        )
        self.mock_post.assert_called_once_with(
            ANY,
            data={
                'updown_id': self.data['upload_id'],
                'binary_filesize': self.data['binary_filesize'],
                'source_uploaded': self.data['source_uploaded'],
            },
            files=[
                ('screenshots', screenshot1),
                ('screenshots', screenshot2),
            ],
        )

    def test_get_upload_url(self):
        with patch.dict(os.environ,
                        MYAPPS_API_ROOT_URL='http://example.com'):
            upload_url = "http://example.com/click-package-upload/app.dev/"
            url = self.command.get_upload_url('app.dev')
            self.assertEqual(url, upload_url)


class UploadCommandTestCase(UploadCommandBaseTestCase):

    def setUp(self):
        super(UploadCommandTestCase, self).setUp()

        patcher = patch('click_toolbelt.upload.Upload.log')
        self.mock_log = patcher.start()
        self.addCleanup(patcher.stop)

        self.package_name = 'namespace.binary'
        self.binary_filename = self.package_name + '_0.1_all.click'
        self.parsed_args = namedtuple(
            'parsed_args',
            'binary_filename, metadata_filename')
        self.args = self.parsed_args(self.binary_filename, None)

    def test_parser(self):
        parser = self.command.get_parser(__namespace__)
        # binary_filename is required
        self.assertEqual(parser._actions[1].dest, 'binary_filename')
        self.assertTrue(parser._actions[1].required)
        # metadata_filename is optional
        self.assertEqual(parser._actions[2].dest, 'metadata_filename')
        # this is a positional argument
        self.assertEqual(parser._actions[2].option_strings, [])
        self.assertFalse(parser._actions[2].required)
        self.assertEqual(parser._actions[3].dest, 'metadata_filename')
        # this is a named argument
        self.assertEqual(parser._actions[3].option_strings, ['--metadata'])
        self.assertFalse(parser._actions[3].required)

    def test_take_action(self):
        binary_filename = self.args.binary_filename

        with patch.multiple(self.command, upload_files=DEFAULT,
                            upload_app=DEFAULT):

            self.command.take_action(self.args)

            self.command.upload_files.assert_called_once_with(binary_filename)
            self.command.upload_app.assert_called_once_with(
                self.package_name, self.command.upload_files.return_value,
                metadata={})
            self.mock_log.info.assert_any_call(
                'Application uploaded successfully.'
            )

    def test_take_action_with_metadata_file(self):
        mock_metadata_file = tempfile.NamedTemporaryFile()
        with open(mock_metadata_file.name, 'wb') as mock_file:
            data = json.dumps({'changelog': 'some changes'})
            mock_file.write(data.encode('utf-8'))
            mock_file.flush()

        with patch.multiple(self.command, upload_files=DEFAULT,
                            upload_app=DEFAULT):

            args = self.parsed_args(self.binary_filename,
                                    mock_metadata_file.name)
            self.command.take_action(args)

            self.command.upload_files.assert_called_once_with(
                self.binary_filename)
            self.command.upload_app.assert_called_once_with(
                self.package_name, self.command.upload_files.return_value,
                metadata={'changelog': 'some changes'})
            self.mock_log.info.assert_any_call(
                'Application uploaded successfully.'
            )

    def test_take_action_with_metadata_file_without_source_file(self):
        mock_metadata_file = tempfile.NamedTemporaryFile()
        with open(mock_metadata_file.name, 'wb') as mock_file:
            data = json.dumps({'changelog': 'some changes'})
            mock_file.write(data.encode('utf-8'))
            mock_file.flush()

        with patch.multiple(self.command, upload_files=DEFAULT,
                            upload_app=DEFAULT):

            args = self.parsed_args(self.binary_filename,
                                    mock_metadata_file.name)
            self.command.take_action(args)

            self.command.upload_files.assert_called_once_with(
                self.binary_filename)
            self.command.upload_app.assert_called_once_with(
                self.package_name, self.command.upload_files.return_value,
                metadata={'changelog': 'some changes'})
            self.mock_log.info.assert_any_call(
                'Application uploaded successfully.'
            )

    def test_take_action_with_error_during_file_upload(self):
        binary_filename = self.args.binary_filename

        with patch.multiple(self.command, upload_files=DEFAULT,
                            upload_app=DEFAULT):

            self.command.upload_files.return_value = {
                'success': False,
                'errors': ['some error']
            }

            with self.assertRaises(CommandError):
                self.command.take_action(self.args)

            self.command.upload_files.assert_called_once_with(
                binary_filename)
            self.assertFalse(self.command.upload_app.called)
            self.mock_log.info.assert_any_call(
                'Upload failed:\n\n%s\n', 'some error')

    def test_take_action_with_error_during_app_upload(self):
        binary_filename = self.args.binary_filename

        with patch.multiple(self.command, upload_files=DEFAULT,
                            upload_app=DEFAULT):

            self.command.upload_app.return_value = {
                'success': False,
                'errors': ['some error'],
            }

            with self.assertRaises(CommandError):
                self.command.take_action(self.args)

            self.command.upload_files.assert_called_once_with(
                binary_filename)
            self.command.upload_app.assert_called_once_with(
                self.package_name, self.command.upload_files.return_value,
                metadata={})
            self.mock_log.info.assert_any_call(
                'Upload did not complete.')
            self.mock_log.info.assert_any_call(
                'Some errors were detected:\n\n%s\n\n',
                'some error')

    def test_take_action_with_invalid_package_name(self):
        with patch.multiple(self.command, upload_files=DEFAULT,
                            upload_app=DEFAULT):

            args = self.parsed_args('binary', None)
            with self.assertRaises(CommandError):
                self.command.take_action(args)

            self.assertFalse(self.command.upload_files.called)
            self.assertFalse(self.command.upload_app.called)
            self.mock_log.info.assert_any_call(
                'Invalid click package filename.')

    def test_take_action_shows_application_url(self):
        with patch.multiple(self.command, upload_files=DEFAULT,
                            upload_app=DEFAULT):

            self.command.upload_app.return_value = {
                'success': True,
                'errors': [],
                'application_url': 'http://example.com/',
            }

            self.command.take_action(self.args)

            self.mock_log.info.assert_any_call(
                'Please check out the application at: %s.\n',
                'http://example.com/')
