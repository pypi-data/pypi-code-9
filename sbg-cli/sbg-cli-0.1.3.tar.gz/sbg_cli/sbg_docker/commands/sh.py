__author__ = 'Sinisa'

import os
import inject
from sbg_cli.config import Config
from sbg_cli.command import Command
from sbg_cli.sbg_docker.docker_client.utils import parse_repo_tag, parse_username, login_as_user, search_image_v1
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
        if not ':' in image:
            image = ':'.join([image, 'latest'])
        img = self.resolve_image(image)
        if not img and len(image.split('/')) == 2:
            img = self.find_image(image)
            if not img:
                print("Can't found  image {}.".format(image))
                return
        print('Creating container from image {}.'.format(img))
        container = self.docker.sh(self.dir, img)
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

    def resolve_image(self, image):
        images = [s for s in self.get_all_images() if image in s]
        if len(images) > 1:
            if self.check_ids(images):
                return images[0]
            else:
                return resolve_conflict(images)
        elif len(images) == 0:
            return None
        return images[0]

    def get_all_images(self):
        repos = []
        images = self.docker.images()
        for img in images:
            repos.extend(img.get('RepoTags', []))
        return repos

    def check_ids(self, images):
        return len(set([self.docker.get_image(a)['Id'] for a in images])) == 1

    def find_image(self, image):
        print('Searching for image {}.'.format(image))
        repo, tag = image.split(':')
        images = None
        docker_hub = None
        if search_image_v1(self.cfg.docker_registry, repo, tag):
            images = '{registry}/{image}'.format(registry=self.cfg.docker_registry, image=image)
        if search_image_v1(self.cfg.docker_hub, repo, tag):
            docker_hub = image
        if all([images, docker_hub]):
            return resolve_conflict([images, docker_hub])
        return images or docker_hub


def resolve_conflict(images):
    print("Multiple images found: ")
    for img in images:
        print(img)
    choice = input('Choose image which you want to run: ').strip()
    return choice