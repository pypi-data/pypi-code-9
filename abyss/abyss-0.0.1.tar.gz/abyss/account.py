#!/usr/bin/env python
''' abyss.player '''

import os
from abyss.db import stored, DB, where, deserialize
from pbkdf2 import PBKDF2

class User(stored):
    __slots__ = ('username', 'hashed_password', 'salt')
    table = DB.table('User')

    def __init__(self, username=None, hashed_password=None, salt=None,
            **kwargs):
        self.username = username
        self.hashed_password = hashed_password
        self.salt = salt

    def for_client(self):
        return {'username': self.username}

    @classmethod
    def from_server(cls, username=None):
        return User(username=username)

    @classmethod
    def get_userdata(cls, username):
        return cls.table.get(where('username') == username)

    @classmethod
    def get_user(cls, username):
        userdata = cls.get_userdata(username)
        if userdata is None:
            return None
        return deserialize(userdata)

    @classmethod
    def authenticate(cls, username, password):
        user = cls.get_user(username)
        if user is None:
            return None
        hashed_password = PBKDF2(
                password, user.salt.decode('base64')).read(32)
        if user.hashed_password.decode('base64') == hashed_password:
            return user
        return None

    @classmethod
    def new(cls, username, password):
        userdata = cls.get_userdata(username)
        if userdata:
            return None
        salt = os.urandom(8)
        hashed_password = PBKDF2(password, salt).read(32)
        user = User(
            username=username, hashed_password=hashed_password.encode('base64'),
            salt=salt.encode('base64')
        )
        user.store()
        return user
