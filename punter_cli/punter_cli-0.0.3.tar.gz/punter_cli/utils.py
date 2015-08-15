"""Utility functions for configuration management."""


import os
import ConfigParser
from punter.exceptions import InvalidAPIKeyException


CONFIG_PATH = os.path.expanduser('~/.punter')


def get_api_key():
    """Return the secret API key.

    Try to return the current secret API key. If there is no config
    file or the requested section cannot be found in the config file
    an empty key is returned.

    :return: The API key.
    :rtype: string

    """    

    config = ConfigParser.SafeConfigParser()
    config.read(CONFIG_PATH)

    try:
        api_key = config.get('secrets', 'key')
    except ConfigParser.NoSectionError:
        api_key = ''

    return api_key


def set_api_key(api_key):
    """Initially set or update the secret API key.

    The secret API key is stored as part of the configuration file
    found in the user's home directory (~/.punter). At present the
    API key is the only config setting stored and read/writes are
    relatively cheap. If and when the configuration settings change
    or grow this will be revisiting. 

    :param api_key: The secret API key.
    :type api_key: string

    """

    config = ConfigParser.SafeConfigParser()
    
    # As the current config is small I don't mind
    # overwriting on each update. Definitely not a
    # long term solution; okay forthe time being.
    with open(CONFIG_PATH, 'w') as configfile:  
        config.add_section('secrets')          
        config.set('secrets', 'key', api_key)
        config.write(configfile)
