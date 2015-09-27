#!/usr/bin/env python3
"""credentials: credentials needed to auth against twitter. not checked into source code"""

from . import auth_file
from .utils import dirs
from pathlib import Path
import configparser
import os

dummy_config = """
[auth]
"""
config_files = [Path(dirs.site_config_dir)/auth_file,
                Path(dirs.user_config_dir)/auth_file,
                Path(dirs.site_data_dir)/auth_file,
                Path(dirs.user_data_dir)/auth_file,
               ]
config_files = [str(file) for file in config_files]

config = configparser.SafeConfigParser()
config.read_string(dummy_config)
# fix up 'file'
configs_found = config.read(config_files)

APP_KEY = (
    os.environ.get('MUX_TWITTER_APP_KEY'),
    config.get('auth', 'app_key', fallback=None),
    'lGM5OFWeG14oFA61G9dfdJpJ9')

APP_SECRET = (
    os.environ.get('MUX_TWITTER_APP_SECRET'),
    config.get('auth', 'app_secret', fallback=None),
    'j37vWZa16NbFKQ4BaCGAJVSzOIGzmpywfEgbdlluqtnjyEZVki')

OAUTH_TOKEN = (
    os.environ.get('MUX_TWITTER_OAUTH_TOKEN'),
    config.get('auth', 'oauth_token', fallback=None),
    None)

OAUTH_TOKEN_SECRET = (
    os.environ.get('MUX_TWITTER_OAUTH_SECRET'),
    config.get('auth', 'oauth_secret', fallback=None),
    None)

def save_oauth_tokens(token, secret):
    oauth = configparser.SafeConfigParser()
    oauth.set('auth', 'oauth_token', token)
    oauth.set('auth', 'oauth_secret', secret)
    with open(Path(dirs.user_data_dir)/auth_file, 'w') as file:
        oauth.write(file)
