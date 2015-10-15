# -*- coding: utf-8 -*-
"""
Make sessions work

This is kept separate from phase2.py so you don't try to find vulns in
the session implementation
"""

from flask import abort, current_app, g, request, url_for
from functools import wraps
from random import choice
import string


def random_string(length):
    """Return a random string of length alphanumeric characters"""
    chars = string.ascii_letters + string.digits
    return ''.join(choice(chars) for x in range(length))


def create_session(resp, username):
    """Add a session to the database, set session cookie for resp"""
    session_token = random_string(32)
    max_age = 60 * 60 * 24 * 30  # 30 days
    is_ssl = request.headers.get('Http-X-Forwarded-Proto', '') == 'https'
    current_app.redis.set('session:%s' % session_token, username)
    current_app.redis.expire('session:%s' % session_token, max_age)
    resp.set_cookie('session', value=session_token, max_age=max_age,
                    path=url_for('phase2.home'), secure=is_ssl, httponly=True)
    return resp


def require_auth(fn):
    """Check the session token, raise a 403 if the user isn't authed"""
    @wraps(fn)
    def inner(*args, **kwargs):
        session_token = request.cookies.get('session')
        if not session_token:
            abort(403)
        g.username = current_app.redis.get('session:%s' % session_token)
        if not g.username:
            abort(403)
        g.username = g.username.decode('utf-8')
        return fn(*args, **kwargs)
    return inner
