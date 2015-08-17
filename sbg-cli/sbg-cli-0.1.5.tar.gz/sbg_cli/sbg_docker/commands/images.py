__author__ = 'Sinisa'

import inject
from sbg_cli.config import Config
from sbg_cli.command import Command
from sbg_cli.sbg_docker.docker_client.client import Docker


class Images(Command):

    cmd = 'docker-images'
    order = 3

    def __init__(self):
        self.docker = inject.instance(Docker)
        self.cfg = inject.instance(Config)


    def __call__(self, *args, **kwargs):
        self.get_images()

    def get_images(self):
        registry = self.cfg.docker_registry
        images = self.docker.images()
        for img in images:
            for repo in img.get('RepoTags', []):
                if repo.startswith(registry):
                    print(repo.replace(registry + '/', ''))
