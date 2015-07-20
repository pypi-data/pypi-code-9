__author__ = 'sinisa'

import os
import sys
import json
from sys import stdout
from subprocess import Popen
from docker.client import Client
from docker.utils import kwargs_from_env
from docker.errors import APIError
from sbg_cli.sbg_docker.docker_client.utils import update_docker_cfg
from sbg_cli.sbg_docker.docker_client.shell import Bash

DEFAULT_DOCKER_API_VERSION = '1.17'
DEFAULT_DOCKER_CLIENT_TIMEOUT = 240
DEFAULT_DOCKER_HOST = 'tcp://192.168.59.103:2376'
DEFAULT_DOCKER_CERT_PATH = os.path.join(os.path.expanduser("~"),
                                        '.boot2docker/certs/boot2docker-vm')
DEFAULT_DOCKER_TLS_VERIFY = '1'

DEFAULT_CONFIG = {
    "version": DEFAULT_DOCKER_API_VERSION,
    "timeout": DEFAULT_DOCKER_CLIENT_TIMEOUT,
}


def set_env():
    docker_host = os.environ.get('DOCKER_HOST', None)
    if not docker_host:
        os.environ['DOCKER_HOST'] = DEFAULT_DOCKER_HOST
    docker_cert_path = os.environ.get('DOCKER_CERT_PATH', None)
    if not docker_cert_path:
        os.environ['DOCKER_CERT_PATH'] = DEFAULT_DOCKER_CERT_PATH
    # docker_tls_verify = os.environ.get('DOCKER_TLS_VERIFY', None)
    os.environ['DOCKER_TLS_VERIFY'] = DEFAULT_DOCKER_TLS_VERIFY


def docker_client_osx(**kwargs):
    set_env()
    env = kwargs_from_env()
    env['tls'].verify = False
    env.update(kwargs)
    return Docker(Client(**env))


def docker_client_linux(**kwargs):
    return Docker(Client(**kwargs))


def create_docker_client(cfg=None):
    if cfg:
        client_config = {
            "version": cfg.docker_client_version,
            "timeout": cfg.docker_client_timeout,
        }
    else:
        client_config = DEFAULT_CONFIG
    if sys.platform.startswith('darwin'):
        client = docker_client_osx(**client_config)
    elif sys.platform.startswith('linux'):
        client = docker_client_linux(**client_config)
    else:
        raise EnvironmentError('Unsupported OS')
    return client


class Docker(object):

    def __init__(self, client):
        self.client = client

    def sh(self, dir, image):
        container = Bash(dir, image).run_shell()
        return container

    def login(self, username, password, registry):
        try:
            res = self.client.login(username, password=password, registry=registry, reauth=True)
            update_docker_cfg(self.client._auth_configs)
        except APIError as e:
            print('Error. {}'.format(e))
            return None
        return res

    def commit(self, container, repository, tag):
        tag = tag or 'latest'
        res = self.client.commit(container, repository=repository, tag=tag)
        return res['Id']

    def push(self, repository, tag):
        tag = tag or 'latest'
        push = Popen(['docker', 'push', ':'.join([repository, tag])], stdout=stdout)
        push.wait()

    def push_cl(self, repository, tag):
        tag = tag or 'latest'
        stream = self.client.push(repository, tag, stream=True, insecure_registry=True)
        for s in stream:
            try:
                line = json.loads(s.decode('utf-8'))
                if line.get('progress'):
                    print("{} Progress: {}".format(line.get('status'), line.get('progress')))
                else:
                    print("{}".format(line.get('status')))
            except Exception:
                print(s)

    def remove_container(self, container):
        try:
            return self.client.remove_container(container)
        except APIError as e:
            print('Error. {}'.format(e.message))

    def remove_image(self, image):
        img = self.get_image(image)
        if img:
            try:
                self.client.remove_image(img, force=True)
            except APIError as e:
                print('Error. {}'.format(e.message))
                return None
            else:
                return img['Id']
        else:
            return None

    def get_image(self, image):
        imgs = self.client.images()
        for img in imgs:
            if image in img['RepoTags']:
                return img
        return None

    def run_command(self, image, cmd):
        pass

    def create_from_dockerfile(self, dockerfile):
        pass

    def version(self):
        return self.client.version()

    def images(self):
        return self.client.images()
