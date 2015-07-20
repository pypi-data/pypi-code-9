__author__ = 'Sinisa'

import os
import inject
from sbg_cli.config import Config
from sbg_cli.command import Command
from sbg_cli.sbg_docker.docker_client.utils import parse_repo_tag, parse_username, login_as_user
from sbg_cli.sbg_docker.docker_client.client import Docker
from sbg_cli.sbg_docker.error import SBGError


try:
    input = raw_input
except NameError:
    pass


class Sh(Command):

    cmd = 'docker-run'
    args = '<image>'
    order = 1

    def __init__(self):
        self.docker = inject.instance(Docker)
        self.cfg = inject.instance(Config)
        self.dir = os.getcwd()

    def __call__(self, *args, **kwargs):
        self.sh(kwargs['<image>'])

    def sh(self, image):
        print('Creating container from image %s' % image)
        container = self.docker.sh(self.dir, image)
        repo, tag = self.ask_commit(container)
        if repo and tag:
            self.ask_push(repo, tag)

    def ask_commit(self, container):
        while True:
            choice = input('Enter project short name and optional tag (eg. jsmith/my_tools:1.3.0) if you want to commit this container. Leave blank to ignore: ').strip()
            if choice != '':
                try:
                    repo, tag = parse_repo_tag(choice)
                except SBGError:
                    print('Commit failed. Invalid repository name')
                    return None, None
                repository = '/'.join([
                    self.cfg.docker_registry, repo]) if (
                    repo and self.cfg.docker_registry) else \
                    repo if repo else None
                tag = tag or 'latest'
                try:
                    image_id = self.docker.commit(container, repository=repository, tag=tag)
                except Exception as e:
                    print('Failed to commit container: %s' % e.__str__())
                else:
                    print("Image id: {}".format(image_id))
                    self.docker.remove_container(container)
                    return repo, tag
            else:
                self.docker.remove_container(container)
                return None, None

    def ask_push(self, repo, tag):
        while True:
            choice = input('Do you want to push this image? [Y/n]: ').lower().strip()
            if choice == '' or choice[0] == 'y':
                username = parse_username(repo)
                repository = '/'.join([
                    self.cfg.docker_registry, repo]
                ) if self.cfg.docker_registry else repo
                if login_as_user(self.docker, self.cfg.docker_registry,
                                 self.cfg.auth_server, username=username, retry=1):
                    self.docker.push_cl(repository, tag)
                else:
                    print('Push failed. Wrong password!')
                return
            elif choice == 'n':
                return
            else:
                print("Please enter 'y' or 'n': ")
