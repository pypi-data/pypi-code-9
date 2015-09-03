#!/usr/bin/env python
import requests
from functools import wraps
from abyss.server import route
from abyss.account import User


BASE_URL = 'http://localhost:8080'

class Client(object):

    def __init__(self, username=None, password=None, base_url=BASE_URL):
        self.auth = (username, password)
        self.url = base_url

    def get_home(self):
        rt = self.url + route('base')
        return requests.get(rt, auth=self.auth).json()

    def get_user(self, username):
        rt = self.url + route('user').format(username=username)
        response = requests.get(rt, auth=self.auth)
        return User.from_server(**response.json())
    
def main():
    import argparse
    parser = argparse.ArgumentParser(prog='abyss')
    parser.add_argument('--username', '-u')
    parser.add_argument('--password', '-p')
    args = parser.parse_args()
    client = Client(username=args.username, password=args.password)
    print client.get_home()
    print client.get_user('foo').username

if __name__ == '__main__':
    main()
