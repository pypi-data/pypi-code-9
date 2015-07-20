__author__ = 'Sinisa'

import os
import json


DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser("~"), '.sbgenomics.conf')

DEFAULT_DOCKER_API_VERSION = '1.17'
DEFAULT_DOCKER_CLIENT_TIMEOUT = 240
DEFAULT_DOCKER_REGISTRY_URL = "images.sbgenomics.com"
DEFAULT_AUTH_SERVER_URL = "https://hatchery.sbgenomics.com"
DEFAULT_APP_REGISTRY_URL = "brood.sbgenomics.com"
DEFAULT_PLATFORM_URL = ("www.sbgenomics.com", 'igor.sbgenomics.com')

DEFAULT_CONFIG = {
    "docker_client_version": DEFAULT_DOCKER_API_VERSION,
    "docker_client_timeout": DEFAULT_DOCKER_CLIENT_TIMEOUT,
    "docker_registry": DEFAULT_DOCKER_REGISTRY_URL,
    "auth_server": DEFAULT_AUTH_SERVER_URL,
    "app_registry": DEFAULT_APP_REGISTRY_URL,
    'platform_url': DEFAULT_PLATFORM_URL
}


def read_config(path):
    cfg = {}
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                cfg = json.load(f)
        except Exception:
            print('Error loading config from %s.' % path)
    return cfg


def load_config():
    cfg = DEFAULT_CONFIG
    config_path = os.environ.get('SBG_CONFIG_FILE', None)
    if config_path:
        external_config = read_config(config_path)
    else:
        external_config = read_config(DEFAULT_CONFIG_PATH)
    cfg.update(external_config)
    return Config(cfg)


class Config(dict):

    def __getattr__(self, attr):
        return self.get(attr)

    __setattr__= dict.__setitem__

    __delattr__= dict.__delitem__