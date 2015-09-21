import datetime
import logging
import os
import select
import shutil

from subprocess import PIPE, STDOUT, Popen

from zymbit.compat import config, util
from zymbit.exceptions import TunnelError
from zymbit.timeutil import now
from zymbit.util import ZymbitApi


SSH = os.environ.get('SSH', '/usr/bin/ssh')
MAX_BACKOFF = 300  # 5 minutes

# how long a connection must be in place in order to consider it okay to clear backoff
CONNECTION_OK_DELTA = datetime.timedelta(seconds=30)


class Tunnel(object):
    defaults = {
        'user': None,
        'host': None,
        'identity_file': config.TUNNEL_SSH_KEY_PATH,
        'ssh_port': None,
        'port': 22,
    }

    def __init__(self, **kwargs):
        _config = self.defaults.copy()
        _config.update(config.get_config().get('tasks', {}).get('tunnel', {}).get('config', {}))
        _config.update(dict([item for item in kwargs.items() if item[1]]))

        unconfigured = [key for key, val in _config.items() if val is None]
        if unconfigured:
            raise TunnelError('{} cannot be unset'.format(unconfigured))

        self.user = _config['user']
        self.host = _config['host']
        self.port = str(_config['port'])
        self.identity_file = _config['identity_file']
        self.ssh_port = str(_config['ssh_port'])

        self.connection = None
        self.connected_at = None

        self.backoff = 0
        self.backoff_until = None

        self.connect()

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def close(self):
        if self.connection is None:
            return

        try:
            self.connection.kill()
        except OSError, exc:
            if exc[0] != 3:
                raise

        self.connection.wait()

        self.connection = None

    def check(self):
        if not self.connection:
            self.connect()
            if self.connection is None:
                self.logger.debug('no connection')
                return

        # this is the main throttling sleep here, keep it at around 1 second
        stdout = self.connection.stdout
        r, _, _ = select.select([stdout], [], [], 0.01)
        for stream in r:
            line = stream.readline().strip()
            if line:
                self.logger.info('line={}'.format(line))

        status = self.connection.poll()
        if status is None:
            # connection is established, see if backoff needs to be reset
            if self.backoff and now() > self.connected_at + CONNECTION_OK_DELTA:
                self.logger.debug('connection ok, resetting backoff')
                self.backoff = 0
                self.backoff_until = None

            return

        # a connection had been established, but has ended, need to reconnect
        self.logger.warning('closing connection after status={}'.format(status))
        self.close()

        # set the backoff time
        self.backoff += 1
        seconds = min(2**self.backoff, MAX_BACKOFF)
        self.backoff_until = now() + datetime.timedelta(seconds=seconds)

        self.logger.debug('backoff={}, seconds={}, backoff_until={}'.format(
            self.backoff, seconds, self.backoff_until))

    def check_host_key(self):
        zymbit_known_hosts = config.ZYMBIT_KNOWN_HOSTS
        known_hosts = config.KNOWN_HOSTS
        if not os.path.exists(known_hosts):
            shutil.copyfile(zymbit_known_hosts, known_hosts)
            return True

        with open(zymbit_known_hosts, 'rb') as zbkh:
            while True:
                pubkey = zbkh.readline()
                if pubkey == '':  # end of file
                    break

                pubkey = pubkey.strip()
                if pubkey == '':  # skip empty lines
                    continue

                known_hosts_temp = '{}.tmp'.format(known_hosts)

                try:
                    line_found = False
                    with open(known_hosts_temp, 'wb') as new_hosts:
                        with open(known_hosts, 'rb') as old_hosts:
                            line = old_hosts.readline().strip()

                            if line == pubkey:
                                line_found = True

                            new_hosts.write('{}\n'.format(line))

                        if not line_found:
                            new_hosts.write('{}\n'.format(pubkey))

                    # overwrite the temporary file
                    shutil.move(known_hosts_temp, known_hosts)
                finally:
                    if os.path.exists(known_hosts_temp):
                        os.remove(known_hosts_temp)

    def connect(self):
        if self.backoff_until and self.backoff_until > now():
            self.logger.debug('not connecting, backoff_until={}'.format(self.backoff_until))
            return

        self.create_ssh_key()
        self.check_host_key()

        self.connection = Popen((
            SSH, '-N', '-I', '60', '-R', self.tunnel_conf,
            '-i', self.identity_file, '-p', self.port, self.remote_server
        ), stdout=PIPE, stderr=STDOUT)

        self.connected_at = now()

        return self.connection

    def create_ssh_key(self):
        _config = config.get_config()
        tunnel_config = _config.setdefault('tunnel', {})
        identity_file = config.TUNNEL_SSH_KEY_PATH
        if not os.path.exists(identity_file):
            util.create_ssh_key(identity_file)
            self.logger.info('created ssh key at identity_file={}'.format(identity_file))

        pubkey = util.get_pubkey(identity_file)
        if pubkey:
            data = dict(
                ssh_pubkey=pubkey
            )

            # post the identity file
            api = ZymbitApi()
            try:
                api.request('post', '/zymbots/{uuid}/pubkey', data=data)
            except ZymbitApi.HTTPError, exc:
                self.logger.exception(exc)
                self.logger.error('Unable to post public key')

        # check to see if config should be written
        if not tunnel_config.get('host'):
            _config['tunnel'].update({
                'user': 'tunnel',
                'host': 'tunnel.zymbit.com',
            })
            config.save_config(_config)

        return True

    def loop(self):
        return self.check()

    def reconnect(self):
        self.close()
        self.connect()

    @property
    def remote_server(self):
        return '{}@{}'.format(self.user, self.host)

    @property
    def tunnel_conf(self):
        return '{}:localhost:22'.format(self.ssh_port)
