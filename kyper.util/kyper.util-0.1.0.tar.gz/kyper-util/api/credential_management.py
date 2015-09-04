# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                                print_function, unicode_literals)
from builtins import *
from future.standard_library import install_aliases
install_aliases()

import json
import logging
import os
import requests
import getpass
import sqlite3
from urllib import parse as urlparse
from functools import update_wrapper

from kyper.util import config
from kyper.util.api.errors import InvalidCredentialsException

_DB_CONN = sqlite3.connect(config.KYPER_DB_LOCATION)

class AuthenticationFailed(Exception):
    pass

class InvalidRefreshToken(Exception):
    pass

class AuthDBDoesNotExist(Exception):
    pass

def _initialize_tokens(username, auth_token, refresh_token):
    cur = _DB_CONN.cursor()
    sql = """CREATE TABLE IF NOT EXISTS credentials(id INT PRIMARY KEY, username TEXT, auth_token TEXT, refresh_token TEXT)"""
    cur.execute(sql)
    sql = """INSERT OR REPLACE INTO credentials VALUES (1, ?, ?, ?)"""
    cur.execute(sql, (username, auth_token, refresh_token))
    _DB_CONN.commit()
    cur.close()

def _get_tokens_from_username_and_password(username, password):
    r = requests.post(urlparse.urljoin(config.AUTH_URL, "authtoken/"), data=json.dumps({
        "email": username, 
        "password": password}),
        headers={'Content-type': 'application/json', 'Accept': 'application/json'},
        allow_redirects=False
    )
    js = r.json()
    if js['status'] == 'ok':
        return (js["auth_token"], js["refresh_token"])
    elif js['name'] == 'AuthenticationFailed':
        raise AuthenticationFailed
    else:
        raise Exception("{}: {}".format(js['name'], js['detail']))

def _clear_tokens():
    cur = _DB_CONN.cursor()
    sql = """DROP TABLE IF EXISTS credentials"""
    cur.execute(sql)
    _DB_CONN.commit()
    cur.close()


def save_tokens(username, auth_token, refresh_token):
    sql = """UPDATE credentials SET username=?, auth_token=?, refresh_token=? WHERE id=1"""
    cur = _DB_CONN.cursor()
    try:
        cur.execute(sql, (username, auth_token, refresh_token))
    except sqlite3.OperationalError:
        _initialize_tokens(username, auth_token, refresh_token)
    _DB_CONN.commit()
    cur.close()

def get_auth_token():
    sql = """SELECT auth_token FROM credentials"""
    cur = _DB_CONN.cursor()
    try:
        row = cur.execute(sql).fetchone()
    except sqlite3.OperationalError:
        raise AuthDBDoesNotExist
    
    if row is None:
        raise AuthDBDoesNotExist
    res = row[0]
    cur.close()
    return res

def get_refresh_token():
    sql = """SELECT refresh_token FROM credentials WHERE id=1"""
    cur = _DB_CONN.cursor()
    try:
        row = cur.execute(sql).fetchone()
    except sqlite3.OperationalError:
        raise AuthDBDoesNotExist

    if row is None:
        raise AuthDBDoesNotExist
    res = row[0]
    cur.close()
    return res

def get_username():
    sql = """SELECT username FROM credentials WHERE id=1"""
    cur = _DB_CONN.cursor()
    try:
        row = cur.execute(sql).fetchone()
    except sqlite3.OperationalError:
        raise AuthDBDoesNotExist

    if row is None:
        raise AuthDBDoesNotExist
    res = row[0]
    cur.close()
    return res


def get_new_credentials():
    '''
        get new authentication/refresh tokens via email/password.
        should only be used if refresh token is expired.
    '''
    print("Please enter your Kyper username and password for access.")
    
    while True:
        username = input("Username: ")
        password = getpass.getpass()
        try:
            auth_token, refresh_token = _get_tokens_from_username_and_password(username, password)
        except AuthenticationFailed:
            print("Your username/password combo was incorrect. Retry:")
            continue

        save_tokens(username, auth_token, refresh_token)
        break

    

def refresh_credentials():
    '''
        perform a global refresh of authentication tokens. requires that a valid refresh token and its associated auth
        token be stored in the in-memory DB
    '''
    r = requests.post(urlparse.urljoin(config.AUTH_URL, "authtoken/"), data=json.dumps({
        "email": get_username(), 
        "auth_token": get_auth_token(), 
        "refresh_token": get_refresh_token()}),
        headers={'Content-type': 'application/json', 'Accept': 'application/json'},
        allow_redirects=False
    )
    js = r.json()

    if js['status'] == 'ok':
        save_tokens(js["email"], js["auth_token"], js["refresh_token"])
    elif js['name'] == 'InvalidRefreshToken':
        raise InvalidRefreshToken
    else:
        raise Exception("{}: {}".format(js['name'], js['detail']))

def refresh_stale_credentials(func):
    def catch_and_call(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidCredentialsException as e:
            logging.warning("Invalid tokens, trying a credentials refresh")
            try:
                refresh_credentials()
            except Exception as e:
                if str(e).split(":")[0] == "InvalidRefreshToken":
                    get_new_credentials()

            return func(*args, **kwargs)

    return update_wrapper(catch_and_call, func)
