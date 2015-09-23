# Copyright 2013 Canonical Ltd.  This software is licensed under the
# GNU General Public License version 3 (see the file LICENSE).
from __future__ import absolute_import, unicode_literals
import json
import logging
import os
import re

from click_toolbelt.common import (
    AuthenticatedCommand,
    CommandError,
    is_scan_completed,
    retry,
)
from click_toolbelt.compat import open, quote_plus, urljoin
from click_toolbelt.constants import (
    CLICK_UPDOWN_UPLOAD_URL,
    MYAPPS_API_ROOT_URL,
    SCAN_STATUS_POLL_DELAY,
    SCAN_STATUS_POLL_RETRIES,
)


class Upload(AuthenticatedCommand):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Upload, self).get_parser(prog_name)

        parser.add_argument('binary_filename')
        metadata_group = parser.add_mutually_exclusive_group()
        metadata_group.add_argument('metadata_filename', nargs='?')
        metadata_group.add_argument('--metadata', metavar='metadata_filename',
                                    dest='metadata_filename')

        return parser

    def take_action(self, parsed_args):
        self.log.info('Running scan-upload command...')

        binary_filename = parsed_args.binary_filename
        metadata_filename = parsed_args.metadata_filename

        success = self.upload_with_scan(binary_filename, metadata_filename)
        if not success:
            # raise an exception to exit with proper code
            raise CommandError()

    def upload_with_scan(self, binary_filename, metadata_filename):

        # validate package filename
        pattern = (r'(.*/)?(?P<name>[\w\-_\.]+)_'
                   '(?P<version>[\d\.]+)_(?P<arch>\w+)\.click')
        match = re.match(pattern, binary_filename)
        if not match:
            self.log.info('Invalid click package filename.')
            return
        name = match.groupdict()['name']

        self.log.info('Uploading files...')
        data = self.upload_files(binary_filename)
        success = data.get('success', False)
        errors = data.get('errors', [])
        if not success:
            self.log.info('Upload failed:\n\n%s\n', '\n'.join(errors))
            return False

        self.log.info('Uploading new version...')
        result = self.upload_app(
            name, data, metadata=self.read_metadata(metadata_filename))
        success = result.get('success', False)
        errors = result.get('errors', [])
        app_url = result.get('application_url', '')

        if success:
            self.log.info('Application uploaded successfully.')
        else:
            self.log.info('Upload did not complete.')

        if errors:
            self.log.info('Some errors were detected:\n\n%s\n\n',
                          '\n'.join(errors))

        if app_url:
            self.log.info('Please check out the application at: %s.\n',
                          app_url)

        return success

    def upload_files(self, binary_filename):
        updown_url = os.environ.get('CLICK_UPDOWN_UPLOAD_URL',
                                    CLICK_UPDOWN_UPLOAD_URL)
        unscanned_upload_url = urljoin(updown_url, 'unscanned-upload/')
        files = {'binary': open(binary_filename, 'rb')}

        result = {'success': False, 'errors': []}

        session = self.get_oauth_session()
        if session is None:
            result['errors'] = ['No valid credentials found.']
            return result

        try:
            response = session.post(
                unscanned_upload_url,
                files=files)
            if response.ok:
                response_data = response.json()
                result.update({
                    'success': response_data.get('successful', True),
                    'upload_id': response_data['upload_id'],
                    'binary_filesize': os.path.getsize(binary_filename),
                    'source_uploaded': 'source' in files,
                })
            else:
                self.log.error(
                    'There was an error uploading the click package.\n'
                    'Reason: %s\n'
                    'Text: %s',
                    response.reason, response.text)
                result['errors'] = [response.text]
        except Exception as err:
            self.log.exception(
                'An unexpected error was found while uploading files.')
            result['errors'] = [str(err)]
        finally:
            # make sure to close any open files used for request
            for fd in files.values():
                fd.close()

        return result

    def read_metadata(self, metadata_filename):
        if metadata_filename:
            with open(metadata_filename, 'r') as metadata_file:
                # file is automatically closed by context manager
                metadata = json.load(metadata_file)
        else:
            metadata = {}

        return metadata

    def upload_app(self, name, upload_data, metadata=None):
        upload_url = self.get_upload_url(name)

        result = {'success': False, 'errors': [], 'application_url': ''}

        session = self.get_oauth_session()
        if session is None:
            result['errors'] = ['No valid credentials found.']
            return result

        if metadata is None:
            metadata = {}

        try:
            data = self.get_post_data(upload_data, metadata=metadata)
            files = self.get_post_files(metadata=metadata)

            response = session.post(upload_url, data=data, files=files)
            if response.ok:
                response_data = response.json()
                status_url = response_data['status_url']
                self.log.info('Package submitted to %s', upload_url)
                self.log.info('Checking package status...')
                completed, data = self.get_scan_data(session, status_url)
                if completed:
                    self.log.info('Package scan completed.')
                    message = data.get('message', '')
                    if not message:
                        result['success'] = True
                    else:
                        result['errors'] = [message]
                else:
                    result['errors'] = [
                        'Package scan took too long.',
                    ]
                    status_web_url = response_data.get('web_status_url')
                    if status_web_url:
                        result['errors'].append(
                            'Please check the status later at: %s.' % (
                                status_web_url),
                        )
                result['application_url'] = data.get('application_url', '')
            else:
                self.log.error(
                    'There was an error uploading the application.\n'
                    'Reason: %s\n'
                    'Text: %s',
                    response.reason, response.text)
                result['errors'] = [response.text]
        except Exception as err:
            self.log.exception(
                'There was an error uploading the application.')
            result['errors'] = [str(err)]
        finally:
            # make sure to close any open files used for request
            for fname, fd in files:
                fd.close()

        return result

    def get_upload_url(self, name):
        myapps_api_url = os.environ.get('MYAPPS_API_ROOT_URL',
                                        MYAPPS_API_ROOT_URL)
        upload_url = urljoin(myapps_api_url, 'click-package-upload/')
        upload_url += "%s/" % quote_plus(name)
        return upload_url

    def get_post_data(self, upload_data, metadata=None):
        data = {
            'updown_id': upload_data['upload_id'],
            'binary_filesize': upload_data['binary_filesize'],
            'source_uploaded': upload_data['source_uploaded'],
        }
        data.update({
            key: value
            for (key, value) in metadata.items()
            if key not in (
                # make sure not to override upload_id, binary_filesize and
                # source_uploaded
                'upload_id', 'binary_filesize', 'source_uploaded',
                # skip files as they will be added to the files argument
                'icon_256', 'icon', 'screenshots',
            )
        })
        return data

    def get_post_files(self, metadata=None):
        files = []

        icon = metadata.get('icon', metadata.get('icon_256', ''))
        if icon:
            icon_file = open(icon, 'rb')
            files.append(('icon_256', icon_file))

        screenshots = metadata.get('screenshots', [])
        for screenshot in screenshots:
            screenshot_file = open(screenshot, 'rb')
            files.append(('screenshots', screenshot_file))

        return files

    def get_scan_data(self, session, status_url):
        # initial retry after 5 seconds
        # linear backoff after that
        # abort after 5 retries
        @retry(terminator=is_scan_completed,
               retries=SCAN_STATUS_POLL_RETRIES,
               delay=SCAN_STATUS_POLL_DELAY,
               backoff=1, logger=self.log)
        def get_status():
            return session.get(status_url)

        response, aborted = get_status()

        completed = False
        data = {}
        if not aborted:
            completed = is_scan_completed(response)
            data = response.json()
        return completed, data
