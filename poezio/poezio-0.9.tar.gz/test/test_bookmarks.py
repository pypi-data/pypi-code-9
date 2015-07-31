"""
Test the bookmarks module
"""

import sys
sys.path.append('src')

import pytest
from slixmpp import JID, Iq
from slixmpp.xmlstream import tostring
from xml.etree import ElementTree as ET
from datetime import timedelta

from bookmarks import Bookmark, BookmarkList
import bookmarks

class config(object):
    def __init__(self):
        self.passwords = {}
    def set_and_save(self, name, value, section):
        if name == 'password':
            self.passwords[section] = value

def test_generate_local_bookmark():
    bookmarks.config = config()

    b = Bookmark('jid@example')
    assert b.local() == 'jid@example:'

    b.nick = 'toto'
    assert b.local() == 'jid@example/toto:'

    b.password = 'titi'
    assert b.local() == 'jid@example/toto:'
    assert bookmarks.config.passwords['jid@example'] == 'titi'

