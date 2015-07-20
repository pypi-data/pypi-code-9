__author__ = 'sinisa'

import os
import six
import json
import base64
import getpass
import requests
from sbg_cli.sbg_docker.error import SBGError


try:
    input = raw_input
except NameError:
    pass


DOCKER_CONFIG_FILENAME = '.dockercfg'


def update_docker_cfg(cfg):
    def convert_to_dockercfg(cfg):
        def encode_auth(username, password):
            return base64.b64encode(six.b(':'.join([username, password]))).decode('utf-8')
        dockercfg = {}
        for repo, auth in six.iteritems(cfg):
            dockercfg[repo] = {'auth': encode_auth(auth['username'], auth['password']), 'email': auth['email']}
        return dockercfg

    config_file = os.path.join(os.environ.get('HOME', '.'), DOCKER_CONFIG_FILENAME)
    with open(config_file, 'w') as outfile:
        json.dump(convert_to_dockercfg(cfg), outfile)


def logout_docker_cfg(repo):
    config_file = os.path.join(os.environ.get('HOME', '.'), DOCKER_CONFIG_FILENAME)
    if os.path.exists(config_file):
        with open(config_file, 'r') as c:
            cfg = json.load(c)
            if cfg.get(repo, None):
                cfg.pop(repo)
        with open(config_file, 'w') as outfile:
            json.dump(cfg, outfile)


def get_session(repo):
    config_file = os.path.join(os.environ.get('HOME', '.'), DOCKER_CONFIG_FILENAME)
    if os.path.exists(config_file):
        with open(config_file, 'r') as c:
            try:
                cfg = json.load(c)
            except Exception:
                return None
            if cfg.get(repo, None):
                return (base64.b64decode(cfg[repo]['auth']).rstrip()).decode('utf-8').split(':')[1]
            else:
                return None
    return None


def parse_repo_tag(name):
    if len(name.split('/')) != 2:
        raise SBGError('Invalid repository name')
    name = name.rstrip()
    if ':' in name:
        repo, tag = name.split(':')
    else:
        repo, tag = name, None
    return repo, tag


def parse_username(name):
    if len(name.split('/')) != 2:
        raise SBGError('Invalid repository name')
    username, rest = name.split('/')
    return username


def get_auth_token(auth_server, username, password):
    url = auth_server + '/auth'
    body = {'username': username, 'password': password}
    headers = {'Content-Type': 'application/json'}
    return requests.post(url, json.dumps(body), headers=headers)


def check_token(auth_server, session, username):
    url = auth_server + '/auth'
    headers = {'session-id': session, 'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)

    if response.status_code in (401, 402):
        return False
    elif response.json().get('username') != username:
        return False
    return True


def login_as_user(client, docker_registry, auth_server, username=None, retry=3):
    if retry == 0:
        return False
    if username:
        print('Username: {}'.format(username))
        usr = username
    else:
        usr = input("Username: ")
    if not usr:
        login_as_user(client, docker_registry, auth_server, username=None, retry=retry-1)
    session = get_session(docker_registry)
    if session:
        if check_token(auth_server, session, usr):
            return True
        else:
            logout_docker_cfg(docker_registry)
    pwd = getpass.getpass()
    response = get_auth_token(auth_server, usr, pwd)
    if response.status_code in (401, 402):
        if retry-1 != 0:
            print('Try again. (retries left {})'.format(retry-1))
        return login_as_user(client, docker_registry, auth_server, username=usr, retry=retry-1)
    token = response.json()['session_id']
    if client.login(usr, token, docker_registry):
        return True
    else:
        return False