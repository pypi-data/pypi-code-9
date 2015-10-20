# -*- encoding: utf-8 -*-
import json
import httplib
import urlparse
import urllib
import hashlib
import os
import glob
import errno
import time

from ucloudclient.utils import api_utils
from ucloudclient import uexceptions


class HTTPClient(object):
    def __init__(self, base_url, debug=None, timing=None):
        self.base_url = base_url
        self.timing = timing
        self.debug = debug
        self.time = []
        o = urlparse.urlsplit(base_url)
        if o.scheme == 'https':
            self.conn = httplib.HTTPSConnection(o.netloc)
        else:
            self.conn = httplib.HTTPConnection(o.netloc)

    def __del__(self):
        self.conn.close()

    def get_timing(self):
        return self.time

    def reset_timing(self):
        self.time = []

    def get(self, resouse, params):
        resouse += "?" + urllib.urlencode(params)
        if self.debug:
            print("DEBUG START>>>>\nRequest: %s%s\n" %
                  (self.base_url, resouse))
        response = None

        try:
            if self.timing:
                start_time = time.time()
            self.conn.request("GET", resouse)
            if self.timing:
                self.time.append(("%s %s" % ('GET', resouse),
                                  start_time, time.time()))

        except Exception as e:
            raise uexceptions.ConnectionRefused(e)

        respones_raw = self.conn.getresponse().read()

        try:
            response = json.loads(respones_raw)
            if self.debug:
                print(
                    "Respone: %s\n<<<<DEBUG END\n" %
                    json.dumps(response, encoding='UTF-8', ensure_ascii=False,
                               indent=2))

        except Exception as e:
            raise uexceptions.NoJsonFound(e)

        if response.get('RetCode') != 0:
            print('Message:%(Message)s\nRetCode:%(RetCode)s' % response)
            raise uexceptions.BadParameters("message: %s /n bad parameters:%s"
                                            % (response.get('Message'),
                                               params))
        return response


class Manager(object):
    def __init__(self, api):
        self.api = api

    def _get(self, body):
        body['PublicKey'] = self.api.public_key
        token = api_utils.get_token(self.api.private_key, body)
        body['Signature'] = token
        return self.api.client.get('/', body)


class CompletionCache(object):
    """The completion cache is how we support tab-completion with ucloudclient.

    The `Manager` writes object IDs and Human-IDs to the completion-cache on
    object-show, object-list, and object-create calls.

    The `ucloud.bash_completion` script then uses these files to provide the
    actual tab-completion.

    The cache directory layout is:

        ~/.ucloudclient/
            <hash-of-pubkey-and-url>/
                <resource>-id-cache
                <resource>-human-id-cache
    """

    def __init__(self, pubkey, url, attributes=('id', 'human_id')):
        self.directory = self._make_directory_name(pubkey, url)
        self.attributes = attributes

    def _make_directory_name(self, username, auth_url):
        """Creates a unique directory name based on the pubkey and url
        of the current user.
        """
        uniqifier = hashlib.md5(username.encode('utf-8') +
                                auth_url.encode('utf-8')).hexdigest()
        base_dir = os.environ.get('UCLOUDCLIENT_UUID_CACHE_DIR',
                                  default="~/.ucloudclient")
        return os.path.expanduser(os.path.join(base_dir, uniqifier))

    def _prepare_directory(self):
        try:
            os.makedirs(self.directory, 0o755)
        except OSError:
            pass

    def clear_class(self, obj_class):
        self._prepare_directory()

        resource = obj_class.__name__.lower()
        resource_glob = os.path.join(self.directory, "%s-*-cache" % resource)

        for filename in glob.iglob(resource_glob):
            try:
                os.unlink(filename)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise

    def _write_attribute(self, resource, attribute, value):
        self._prepare_directory()

        filename = "%s-%s-cache" % (resource, attribute.replace('_', '-'))
        path = os.path.join(self.directory, filename)

        with open(path, 'a') as f:
            f.write("%s\n" % value)

    def write_object(self, obj):
        resource = obj.__class__.__name__.lower()

        for attribute in self.attributes:
            value = getattr(obj, attribute, None)
            if value:
                self._write_attribute(resource, attribute, value)
