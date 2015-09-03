#!/usr/bin/env python

import os
import json
from functools import wraps

from flask import Flask, request

from abyss.server import Route
from abyss.account import User

app = Flask('abyss')

def check_auth(auth):
    if not auth:
        return None
    return User.authenticate(auth['username'], auth['password']) 

def routed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        kwargs['authuser'] = check_auth(auth)
        ret = func(*args, **kwargs)
        return json.dumps(ret)
    return wrapper

@app.route(Route.BASE)
@routed
def index(authuser=None):
    return {'username': authuser.username if authuser else None}

@app.route(Route.USER)
@routed
def user(username, authuser=None):
    user = User.get_user(username)
    if user:
        user = user.for_client()
    return user

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-H', default='127.0.0.1')
    parser.add_argument('--port', '-p', type=int, default=8080)
    parser.add_argument('--debug', '-d', action='store_true')
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()
