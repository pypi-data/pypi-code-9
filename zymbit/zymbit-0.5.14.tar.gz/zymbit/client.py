from __future__ import absolute_import

import Queue
import logging
import os
import random
import select
import socket
import ssl
import time
import datetime

import requests

from .exceptions import NotConnected, ProvisionError
from .websocket import WebSocketConnectionClosedException
from zymbit.clientid import get_client_id

from zymbit.compat import util, config
from zymbit.util import get_connection, get_device_meta
from zymbit.envelope import get_envelope
from zymbit.timeutil import now

MAX_BACKOFF = 300  # 5 minutes
BACKOFF_JITTER = 10  # 10 seconds
CONNECTION_SETTLE_DT = datetime.timedelta(seconds=10)  # 10 second minimum to clear backoff

PROVISION_PATH = os.environ.get('PROVISION_PATH', '/provision')


def get_logger():
    return logging.getLogger(__name__)


def register(provisioning_token=None):
    logger = get_logger()

    client_id = get_client_id()
    _config = config.get_config()

    provisioning_token = provisioning_token or config.get_config().lookup('auth.provisioning_token')
    if not provisioning_token:
        raise ProvisionError('Provisioning token not found')

    logger.debug('provisioning, client_id={}'.format(client_id))

    data = {
        'token': provisioning_token,
        'client_id': client_id,
    }

    data.update(get_device_meta())

    # TODO: update to use ZymbitApi object
    provision_url = '{}{}'.format(_config.lookup('cloud.api_url'), config.PROVISION_PATH)
    verify = _config.lookup('cloud.check_hostname')
    try:
        response = requests.post(provision_url, data=data, verify=verify)
    except requests.ConnectionError, exc:
        logger.exception(exc)
        logger.error('error making request to provision_url={}'.format(provision_url))

        raise

    try:
        response.raise_for_status()
    except requests.HTTPError, exc:
        logger.exception(exc)
        logger.error('error making request to provision_url={}, content={}'.format(
            provision_url, response.content)
        )

        raise

    response_data = response.json()

    return response_data


class Client(object):
    def __init__(self, handle_disconnect=True, connected_callback=None, client_id=None):
        """
        :param handle_disconnect - bool: internally handle a disconnect an gracefully reconnect; raises exception when False
        :return:
        """
        self.client_id = client_id

        self._connected_callback = connected_callback

        self.handle_disconnect = handle_disconnect

        self._ws = None
        self.is_connected = False
        self.connected_at = None

        self.backoff = 0
        self.backoff_until = None

        self.recv_q = Queue.Queue()

    @property
    def logger(self):
        return logging.getLogger(__name__)

    @property
    def check_hostname(self):
        _config = config.get_config()

        return _config.get('cloud', {}).get('check_hostname')

    def connect(self):
        # simply call the ws property that takes care of establishing a connection
        return self.ws

    @property
    def credentials(self):
        env_uuid = os.environ.get('ZYMBIT_AUTH_UUID')
        env_token = os.environ.get('ZYMBIT_AUTH_TOKEN')
        env_client_id = os.environ.get('ZYMBIT_CLIENT_ID')

        if env_uuid and env_token:
            auth = {
                'uuid': env_uuid,
                'auth_token': env_token,
            }
        else:
            _config = config.get_config()
            client_id = env_client_id or get_client_id()

            auth = _config.get('auth', {}).get(client_id)

        return auth

    def _clear_backoff(self):
        if self.connected_at is None:
            return

        # only clear backoff when the connection has been established for more than CONNECTION_SETTLE
        if now() > self.connected_at + CONNECTION_SETTLE_DT:
            self.logger.debug(
                'connected more than {} clearing backoff'.format(CONNECTION_SETTLE_DT)
            )

            self.connected_at = None
            self.backoff = 0
            self.backoff_until = None

            return True

    def close(self):
        # don't close on closed
        if self._ws is None:
            return

        # self._ws.close()
        self.is_connected = False
        self._ws = None

        cleared = self._clear_backoff()
        if not cleared:
            self.backoff += 1
            seconds = min(2**self.backoff, MAX_BACKOFF)
            jitter = datetime.timedelta(seconds=BACKOFF_JITTER*random.random())
            self.backoff_until = jitter + now() + \
                                 datetime.timedelta(seconds=seconds)

            self.logger.debug('backoff={}, backoff_until={}, jitter={}'.format(self.backoff, self.backoff_until, jitter))

    def connected(self):
        """
        Called when websocket connection is initialized
        """
        self.is_connected = True

        self.connected_at = now()
        if self._connected_callback:
            self._connected_callback()

    def fileno(self):
        return self.ws.sock.fileno()

    def recv(self, ws=None):
        ws = ws or self.ws
        sock = ws.sock

        # check if there are pending messages in the queue
        try:
            return self.recv_q.get_nowait()
        except Queue.Empty:
            pass

        r, _, _ = select.select([sock], [], [], 0.01)
        if sock not in r:
            return

        try:
            return ws.recv()
        except WebSocketConnectionClosedException, exc:
            self.close()

            if not self.handle_disconnect:
                raise
        except NotConnected:
            if not self.handle_disconnect:
                raise
        except ssl.SSLError, exc:
            # SSLError: [Errno 8] _ssl.c:1359: EOF occurred in violation of protocol -- arduino
            error_number = exc[0]
            if error_number not in (2, 8):
                self.logger.warning('ssl error #{}, closing connection'.format(error_number))

            self.close()
            if not self.handle_disconnect:
                raise
        except socket.error as exc:
            error_number = exc[0]
            if error_number not in (11, 54):
                self.logger.warning('got socket error {}'.format(error_number))

            self.close()
            if not self.handle_disconnect:
                raise

    def send(self, action, params=None):
        """
        Wrap the given action and params in an envelope and send

        This calls the get_envelope() utility prior to sending the given message.

        :param action: string - upstream action
        :param params: dictionary - contains any data for this action

        :return: the result of send_raw()
        """
        return self.send_raw(get_envelope(action, params=params, client_id=self.client_id))

    def send_raw(self, message):
        """
        Send raw message

        Do not wrap in an envelope; simply send what was passed in

        :param message: string
        :return: result of websocket.send()
        """
        try:
            return self.ws.send(message)
        except socket.error, exc:
            # error: [Errno 131] Connection reset by peer -- arduino
            error_number = exc[0]
            if error_number not in (32, 131):
                self.logger.exception(exc)
                self.logger.warning('socket error_number={}'.format(error_number))

            self.close()

            if not self.handle_disconnect:
                raise

            return False
        except WebSocketConnectionClosedException:
            self.close()

            if not self.handle_disconnect:
                raise

            return False  # the message was not sent

    @property
    def url(self):
        _config = config.get_config()

        return _config.lookup('cloud.websocket_url')

    @property
    def ws(self):
        if self.backoff_until and self.backoff_until > now():
            raise NotConnected()

        if self._ws is not None:
            return self._ws

        try:
            self._ws = get_connection(url=self.url, credentials=self.credentials, check_hostname=self.check_hostname)
        except socket.error, exc:
            # error: [Errno 146] Connection refused -- arduino yun
            # error: [Errno 145] Connection timed out -- arduino yun
            # error: [Errno 148] No route to host -- arduino yun
            # gaierror: [Errno -2] Name or service not known -- arduino yun
            # error: [Errno 131] Connection reset by peer -- arduino yun
            error_number = exc[0]
            self.logger.warning('unable to connect to url={}, socket.error number {}'.format(self.url, error_number))

            self.close()
            raise NotConnected(exc)

        for _ in range(1000):
            try:
                message = self.recv(ws=self._ws)  # prevent recv() from calling this property
            except Exception, exc:
                raise

            # self.recv() may close the connection, so check if _ws is not None
            if self._ws is None or not self._ws.connected:
                self.close()
                raise NotConnected('connection closed on opening')

            if message:
                self.recv_q.put_nowait(message)

                self.logger.debug('message={}'.format(message))
                self.connected()

                break

            time.sleep(0.01)
        else:
            self.close()

            raise NotConnected('unable to get websocket connection')

        self.logger.debug('got websocket, _ws={}'.format(self._ws))

        return self._ws
