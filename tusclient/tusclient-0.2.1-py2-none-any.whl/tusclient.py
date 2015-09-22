import os
import json
import time
import base64
import logging
import hashlib
import httplib
import requests
from urlparse import urlparse, urlunparse

logger = logging.getLogger('TusClient')
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)


class Error(Exception):
    pass


class ServerError(Error):
    pass


class ClientError(Error):
    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason


def parse_rfc_7231_datatime(string):
    try:
        # IMF-fixdate: Sun, 06 Nov 1994 08:49:37 GMT
        ts = time.strptime(string, '%a, %d %b %Y %H:%M:%S GMT')
    except ValueError:
        try:
            # RFC 850 format: Sunday, 06-Nov-94 08:49:37 GMT
            ts = time.strptime(string, '%A, %d-%b-%y %H:%M:%S GMT')
        except ValueError:
            try:
                # ANSI C's asctime() format: Sun Nov  6 08:49:37 1994
                ts = time.strptime(string, '%a %b %d %H:%M:%S %Y')
            except ValueError:
                raise ServerError('Invalid header: Upload-Expires')
    return time.mktime(ts)


class TusClient(object):
    version = '1.0.0'
    upload_finished = False
    upload_max_chunk = 2 ** 10   # 2K
    checksum_algorisum = 'sha1'
    extensions = [
        'creation',
        'expiration',
        'termination',
        'checksum',
        # 'creation-defer-length',     # todo
        # 'checksum-trailer',          # todo
        # 'concatenation',             # todo
        # 'concatenation-unfinished',  # todo
    ]

    def __init__(self, fpath, upload_url, tmp_dir='/tmp/upload', upload_metadata=None):
        self.fpath = os.path.abspath(fpath)
        self.tmp_dir = tmp_dir
        self.info_path = os.path.join(tmp_dir, base64.standard_b64encode(fpath.encode()))
        self.upload_url = upload_url
        assert upload_metadata is None or isinstance(upload_metadata, dict)
        self.upload_metadata = upload_metadata or dict()
        self.values = dict()

        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

    def run(self):
        try:
            self.check_upload()
            if self.is_uploading():
                self.update_values()
            else:
                self.create_file()
            while not self.upload_finished:
                self.upload_file_chunk()
        except ClientError as e:
            logger.exception('Server return: %s %s', e.status_code, e.reason)
        except Error:
            logger.exception('Server Error')
        self.clean_info_file()

    def check_upload(self):
        resp = requests.options(self.upload_url)
        if resp.status_code != httplib.NO_CONTENT:
            raise ClientError(resp.status_code, resp.reason)

        tus_versions = resp.headers.get('Tus-Version')
        tus_max_size = resp.headers.get('Tus-Max-Size')
        tus_extensions = resp.headers.get('Tus-Extension')

        server_conf = dict()
        if tus_versions:
            server_conf['tus_versions'] = [x.strip() for x in tus_versions.split(',')]
        if tus_max_size:
            server_conf['tus_max_size'] = tus_max_size
        if tus_extensions:
            server_conf['tus_extensions'] = [x.strip() for x in tus_extensions.split(',')]
        self.values['server_conf'] = server_conf

        if not os.path.exists(self.fpath):
            raise Error('Not found upload file: %s' % self.fpath)
        if not os.path.isfile(self.fpath):
            raise Error('Upload only for regular file')
        if tus_versions and self.version not in tus_versions:
            raise ServerError('Not implemented version')

    def create_file(self):
        server_conf = self.values['server_conf']
        if 'tus_extensions' in server_conf and 'creation' not in server_conf['tus_extensions']:
            raise ServerError('Not implemented extension: creation')
        upload_length = os.path.getsize(self.fpath)
        if 'tus_max_size' in server_conf and upload_length > server_conf['tus_max_size']:
            raise Error('Max-size Exceeded')
        upload_metadata = {
            'filename': os.path.basename(self.fpath),
        }
        upload_metadata.update(self.upload_metadata)

        info = dict()
        info['fpath'] = self.fpath
        info['upload_metadata'] = upload_metadata
        info['last_modify'] = os.stat(self.fpath).st_mtime
        headers = {
            'Tus-Resumable': self.version,
            'Upload-Length': upload_length,
            'Upload-Metadata': ','.join(['%s %s' % (k, base64.standard_b64encode(v)) for k, v in upload_metadata.items()])
        }
        resp = requests.post(self.upload_url, headers=headers)
        if resp.status_code != httplib.CREATED:
            raise ClientError(resp.status_code, resp.reason)

        location = resp.headers.get('Location')
        if not location:
            raise ServerError('Missing header: Location')
        url = urlparse(location)
        if url.scheme and url.hostname:
            info['location'] = location
        else:
            info['location'] = urlunparse(urlparse(self.upload_url)[:2] + urlparse(location)[2:])
        self.values['upload_offset'] = 0
        self.values['upload_length'] = upload_length
        self.values['info'] = info
        self.update_expires(resp)
        self.update_info_file()

    def update_values(self):
        url = self.get_resource_url()
        headers = {
            'Tus-Resumable': self.version,
        }
        resp = requests.head(url, headers=headers)
        if resp.status_code != httplib.OK:
            raise ClientError(resp.status_code, resp.reason)
        self.update_offset(resp)
        self.update_length(resp)

    def upload_file_chunk(self):
        with open(self.info_path, 'r') as f:
            info = json.load(f)
        if self.fpath != info['fpath'] or os.stat(self.fpath).st_mtime != info['last_modify']:
            raise Error('File changed when uploading')

        url = self.get_resource_url()
        headers = {
            'Tus-Resumable': self.version,
            'Content-Type': 'application/offset+octet-stream',
            'Upload-Offset': self.values['upload_offset'],
        }

        server_conf = self.values['server_conf']
        with open(self.fpath, 'rb') as f:
            f.seek(self.values['upload_offset'], os.SEEK_SET)
            if 'checksum' in server_conf['tus_extensions']:
                data = f.read(self.upload_max_chunk)
                checksum = hashlib.sha1(data).digest()
                headers['Upload-Checksum'] = self.checksum_algorisum + ' ' + base64.standard_b64encode(checksum)
            else:
                data = f.read()

        resp = requests.patch(url, data=data, headers=headers)
        if resp.status_code == httplib.NO_CONTENT:
            self.update_offset(resp)
            self.update_expires(resp)
            self.update_info_file()
            if self.values['upload_offset'] == self.values['upload_length']:
                self.upload_finished = True
            return
        if resp.status_code == httplib.OK:
            self.upload_finished = True
            return
        raise ClientError(resp.status_code, resp.reason)

    def update_offset(self, resp):
        upload_offset = resp.headers.get('Upload-Offset')
        if not upload_offset:
            raise ServerError('Missing header: Upload-Offset')
        try:
            offset = int(upload_offset)
        except ValueError:
            raise ServerError('Invalid header: Upload-Offset')
        if offset < 0:
            raise ServerError('Invalid header: Upload-Offset')
        self.values['upload_offset'] = offset

    def update_length(self, resp):
        upload_length = resp.headers.get('Upload-Length')
        if not upload_length:
            raise ServerError('Missing header: Upload-Length')
        try:
            length = int(upload_length)
        except ValueError:
            raise ServerError('Invalid header: Upload-Length')
        if length < 0:
            raise ServerError('Invalid header: Upload-Length')
        local_length = os.path.getsize(self.fpath)
        if local_length != length:
            raise Error('File changed when uploading')
        self.values['upload_length'] = length

    def update_expires(self, resp):
        server_conf = self.values['server_conf']
        if 'expiration' not in server_conf['tus_extensions']:
            return
        expires = resp.headers.get('Upload-Expires')
        if not expires:
            raise ServerError('Missing header: Upload-Offset')
        self.values['info']['expires'] = parse_rfc_7231_datatime(expires)

    def update_info_file(self):
        with open(self.info_path, 'w') as f:
            json.dump(self.values['info'], f, indent=4)

    def cancel_upload(self):
        self.clean_info_file()
        server_conf = self.values['server_conf']
        if 'termination' not in server_conf:
            return
        url = self.get_resource_url()
        headers = {
            'Tus-Resumable': self.version,
        }
        resp = requests.delete(url, headers=headers)
        if resp.status_code != httplib.NO_CONTENT:
            raise ClientError(resp.status_code, resp.reason)

    def is_uploading(self):
        for fn in os.listdir(self.tmp_dir):
            fp = os.path.join(self.tmp_dir, fn)
            if not os.path.isfile(fp):
                continue
            with open(fp, 'r') as f:
                info = json.load(f)
            if self.fpath == info['fpath'] and os.stat(self.fpath).st_mtime == info['last_modify']:
                self.values['info'] = info
                return True
        return False

    def clean_info_file(self):
        try:
            os.remove(self.info_path)
        except OSError:
            pass

    def get_resource_url(self):
        return self.values['info']['location']
