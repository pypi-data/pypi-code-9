__author__ = 'Sinisa'

import inject
from sbg_cli.config import Config
from sbg_cli.command import Command
from sbg_cli.sbg_docker.docker_client.utils import parse_repo_tag, parse_username, login_as_user
from sbg_cli.sbg_docker.docker_client.client import Docker
from sbg_cli.sbg_docker.error import SBGError


class Push(Command):

    cmd = 'docker-push'
    args = '<owner/project:tag>'
    order = 4

    def __init__(self):
        self.docker = inject.instance(Docker)
        self.cfg = inject.instance(Config)

    def __call__(self, *args, **kwargs):
        project = kwargs.get('<owner/project:tag>')
        try:
            repo, tag = parse_repo_tag(project)
        except SBGError:
            print('Push failed. Invalid repository name.')
            return
        if not tag:
            self.push(repo)
        else:
            self.push(repo, tag=tag)

    def push(self, repo, tag='latest'):
        repository = '/'.join([
            self.cfg.docker_registry, repo]
        ) if self.cfg.docker_registry else repo
        username = parse_username(repo)
        print('Pushing {}'.format(':'.join([repo, tag])))
        if login_as_user(self.docker, self.cfg.docker_registry,
                         self.cfg.auth_server, username=username, retry=1):
            self.docker.push_cl(repository, tag)
        else:
            print('Push failed. Wrong password.')
