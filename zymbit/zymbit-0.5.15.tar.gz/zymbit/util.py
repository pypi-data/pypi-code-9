from __future__ import absolute_import
import argparse
from collections import OrderedDict
import logging
import os
import re
import socket
import subprocess
import sys
import urllib

import pkg_resources
import requests

import zymbit

from .websocket import websocket
from zymbit.clientid import get_client_id
from zymbit.common.config import get_config



# TODO: look into flankr instead of this
# http://blog.mailgun.com/we-just-open-sourced-flanker-our-python-email-address-and-mime-parsing-library/
EMAIL_ADDRESS_RE = re.compile(r'.+@.+\..+')


def find_cpuinfo(markers):
    # no support for non-linux systems
    if os.path.exists('/proc/cpuinfo'):
        content = open('/proc/cpuinfo', 'rb').read()
        for marker, return_value in markers.items():
            if marker in content:
                return return_value


def get_connection(url=None, credentials=None, check_hostname=None):
    headers = []

    logger = logging.getLogger(__name__)

    _config = get_config()

    check_hostname = check_hostname or _config.lookup('cloud.check_hostname')

    sslopt = {"check_hostname": check_hostname}

    url = url or _config.lookup('cloud.websocket_url')
    request_url = url
    if credentials:
        connector_version = get_connector_version()

        credentials.update({
            'hostname': socket.gethostname(),
            'connector_version': connector_version,
        })

        credentials.update(get_device_meta())

        encoded = urllib.urlencode(credentials)
        request_url = '{}?{}'.format(url, encoded)

    logger.debug('getting websocket connection at url={}'.format(url))

    ws = websocket.create_connection(request_url, header=headers, sslopt=sslopt)
    ws.settimeout(0)

    return ws


def get_connector_version():
    try:
        connector_version = pkg_resources.require('zymbit')[0].version
    except pkg_resources.DistributionNotFound:
        # fall back to parsing directory names
        dirname = os.path.dirname(zymbit.__file__)
        packages_dir, package_name = os.path.split(dirname)

        needle = '{}-'.format(package_name)
        for item in os.listdir(packages_dir):
            metadir = os.path.basename(item)
            if metadir.startswith(needle) and metadir.endswith('.egg-info'):
                package_metadir = metadir
                break
        else:
            logging.getLogger(__name__).warning('unable to find zymbit version')
            return

        # parse the metadir name
        metasplit = package_metadir.split('-')
        connector_version = metasplit[1]

    return connector_version


def get_device_meta():
    device_meta = {}

    try:
        # TODO: support linux
        # this didn't work on a server container, so just removed this altogether
        # because these params are intended for additional device metadata, but it
        # would be great to be able to get this from any system.
        from .compat import util
    except ImportError:
        pass
    else:
        device_meta.update({
            'distro': util.get_distro(),
            'model': util.get_model(),
            'system': util.get_system(),
        })

    return device_meta


def get_model():
    systems = OrderedDict((
        ('Arduino Yun', 'yun'),
        ('BCM2708', '1'),
        ('BCM2709', '2'),
    ))
    cpuinfo = find_cpuinfo(systems)
    if cpuinfo:
        return cpuinfo

    if sys.platform == 'darwin':
        return sys.platform


def get_provisioning_token(config=None):
    api = ZymbitApi(config=config)
    response = api.request('get', '/organizations')

    data = response.json()
    organization = data['results'][0]
    provisioning_group = organization['provisioning_groups'][0]

    return provisioning_group['token']


def get_system():
    systems = OrderedDict((
        ('Arduino Yun', 'arduino'),
        ('BCM270', 'raspberrypi'),  # note this will match BCM2708 (rpi) and BCM2709 (rpi2)
    ))
    cpuinfo = find_cpuinfo(systems)
    if cpuinfo:
        return cpuinfo

    if sys.platform == 'darwin':
        return sys.platform

    if 'linux' in sys.platform:
        return 'linux'


def is_interactive():
    import __main__ as main
    return hasattr(main, '__file__')


def run_command(command):
    return subprocess.Popen(command).wait()


def validate_email(address):
    """
    verify the email address given is valid
    :param address: string - an email address
    :return: address or raise an exception
    """
    matches = EMAIL_ADDRESS_RE.match(address)
    if matches is None:
        raise argparse.ArgumentTypeError('address={} does not appear to be valid'.format(address))

    return address


class ZymbitApi(object):
    ConnectionError = requests.ConnectionError
    HTTPError = requests.HTTPError

    def __init__(self, config=None):
        self.response = None
        self._config = config

    @property
    def config(self):
        return self._config or get_config()

    def request(self, method, endpoint, data=None):
        config = self.config

        try:
            auth_key = config['auth']['default_auth']
        except KeyError:
            auth_key = get_client_id()

        auth_config = config['auth'][auth_key]
        api_url = config['cloud']['api_url']

        if '{' in endpoint and '}' in endpoint:
            endpoint = endpoint.format(**auth_config)

        verify = config['cloud'].get('check_hostname', True)

        request_kwargs = dict(
            data=data,
            verify=verify,
        )

        if 'password' in auth_config:
            password = auth_config['password']

            request_kwargs.update(dict(
                auth=(auth_key, password),
            ))
        elif 'auth_token' in auth_config:
            request_kwargs.update(dict(
                headers=dict(
                    Authorization='Token {}'.format(auth_config['auth_token'])
                ),
            ))

        url = '{}{}'.format(api_url, endpoint)

        method_fn = getattr(requests, method)
        try:
            self.response = method_fn(url, **request_kwargs)
        except requests.ConnectionError, exc:
            raise requests.ConnectionError('Unable to connect to url={}'.format(url))
        else:
            self.response.raise_for_status()

        return self.response
