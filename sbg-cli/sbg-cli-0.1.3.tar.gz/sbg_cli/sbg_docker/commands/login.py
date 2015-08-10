__author__ = 'Sinisa'

import inject
import getpass
from sbg_cli.config import Config
from sbg_cli.command import Command
from sbg_cli.sbg_docker.docker_client.client import Docker
from sbg_cli.sbg_docker.docker_client.utils import login_as_user


class Login(Command):

    cmd = 'login'
    order = 0

    def __init__(self):
        self.docker = inject.instance(Docker)
        self.cfg = inject.instance(Config)

    def __call__(self, *args, **kwargs):
        if login_as_user(self.docker, self.cfg.docker_registry,
                         self.cfg.auth_server, username=None, retry=3):
            print('You have been successfully logged in.')
        else:
            print('Failed to login.')
