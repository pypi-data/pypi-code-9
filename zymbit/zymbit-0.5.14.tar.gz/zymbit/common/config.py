import json
import logging
import os
import requests
import stat

from conversion import convert_bool
from zymbit.clientid import get_client_id

AUTH_TOKEN_ENDPOINT = '/auth_token'
PROVISION_PATH = os.environ.get('PROVISION_PATH', '/provision')

TUNNEL_SSH_KEY_PATH = os.path.expanduser(os.environ.get('TUNNEL_SSH_KEY_PATH', '~/.ssh/id_tunnel'))

INIT_SCRIPT_PATH = '/etc/init.d/zymbit'
FILES_ROOT = None

LOGFILE = '/var/log/zymbit.log'

# setup a chain of configurations to try
CONFIG_PATH = os.environ.get('CONFIG_PATH')
if CONFIG_PATH:
    CONFIG_PATHS = (
        CONFIG_PATH,
    )
else:
    CONFIG_PATHS = (
        '/etc/zymbit.conf',
        os.path.expanduser('~/.zymbit.conf'),
    )


def get_logger():
    return logging.getLogger(__name__)


class ConfigError(Exception):
    pass


class ConfigDict(dict):
    def lookup(self, path):
        section = self

        for item in path.split('.'):
            section = section.get(item)
            if section is None:
                break

        # return True/False as is
        if isinstance(section, bool):
            return section

        return section


def get_auth_token(username, password):
    config = get_config()

    api_url = config.lookup('cloud.api_url')
    verify = config.lookup('cloud.check_hostname')
    url = '{}{}'.format(api_url, AUTH_TOKEN_ENDPOINT)
    params = {
        'username': username,
        'password': password,
    }

    response = requests.post(url, data=params, verify=verify)
    response.raise_for_status()

    token_data = response.json()

    return token_data['token']


def get_config():
    logger = get_logger()

    config = ConfigDict({
        'cloud': {
            'api_url': os.environ.get('API_URL', 'https://zymbit.com/api/v1'),
            'check_hostname': convert_bool(os.environ.get('SSL_CHECK_HOSTNAME', 'true')),
            'websocket_url': os.environ.get('WEBSOCKET_URL', 'wss://ws.zymbit.com/channel'),
        }
    })

    for config_path in CONFIG_PATHS:
        if os.path.exists(config_path):
            try:
                _config = json.load(open(config_path, 'rb'))
            except ValueError:
                logger.warning('Unable to load config at {}'.format(config_path))
            else:
                config.update(_config)

    return config


def save_auth(auth_data, password):
    config = get_config()

    email = auth_data['email']
    auth_data['password'] = password

    auth_config = config.setdefault('auth', {})

    auth_config['default_auth'] = email
    auth_config[email] = auth_data

    # request an auth token
    try:
        auth_token = get_auth_token(email, password)
    except requests.HTTPError:
        raise
    else:
        auth_data['auth_token'] = auth_token

    # check for a device token
    client_id = get_client_id()
    if client_id not in auth_config:
        from zymbit.client import register
        from zymbit.util import get_provisioning_token

        provisioning_token = get_provisioning_token(config=config)

        device_config = register(provisioning_token=provisioning_token)
        auth_config[client_id] = device_config['auth'][client_id]

    save_config(config)


def save_config(config):
    logger = logging.getLogger(__name__)

    serialized = json.dumps(config)

    for config_path in CONFIG_PATHS:
        try:
            with open(config_path, 'wb') as fh:
                fh.write(serialized)

            os.chmod(config_path, stat.S_IRUSR | stat.S_IWUSR)
        except IOError, exc:
            # IOError: [Errno 13] Permission denied: '[...]'
            if exc[0] != 13:
                raise
        else:
            logger.debug('config saved at {}'.format(config_path))
            break
    else:
        raise ConfigError('unable to save configuration at any location: {}'.format(CONFIG_PATHS))
