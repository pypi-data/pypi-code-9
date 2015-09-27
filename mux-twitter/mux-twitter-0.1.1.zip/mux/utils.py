#!/usr/bin/env python

from contextlib import contextmanager
from functools import partial
from blessed import Terminal
from appdirs import AppDirs
from twython import Twython
from pathlib import Path
import asyncio
import atexit
import sys, os

from . import program_name

dirs = AppDirs(program_name.capitalize(), "BlitzWorks")

err_print = partial(print, file=sys.stderr)

@contextmanager
def scoped_unlink(file):
    """Delete a file once it is no longer in use, safe even if interpreted exits with sys.exit"""
    @atexit.register
    def delete_temp_file():
        os.unlink(file.name)
        
    try:
        yield file
    finally:
        atexit.unregister(delete_temp_file)
        delete_temp_file()


def get_editor():
    for var_name in EDITOR_ORDER:
        if var_name in os.environ:
            return os.environ[var_name]

    PATH = os.environ.get('PATH', '')

    if PATH:
        path = PATH.split(os.pathsep)
        for editor in FALLBACK_EDITORS:
            for dir in path:
                dir = Path(dir)
                if os.access(dir/editor, os.X_OK):
                    return editor


def get_terminal_width():
    term = Terminal()
    width = os.environ.get('WIDTH') or term.width or 80

    return width

def get_credentials():
    """Grab the twitter authenticaiton details"""
    OAUTH_TOKEN = os.environ['MUX_TWITTER_OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = os.environ['MUX_TWITTER_OAUTH_TOKEN_SECRET']

    return APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET

def get_twitter():
    """Grab the authentication details from some unknown location and return a proxy for twitter"""
    auth = get_credentials()

    twitter = Twython(*auth)

    return twitter
