"""Cleans up the environment by destroying temporary container and images.
"""
from __future__ import print_function
import os

import docker

from ..config import Config


NEEDS_ENVIRONMENT = True


def add_command_line_arguments(parser, _environ):
    parser.add_argument('-q',
        help='No verbose output. Only print errors.',
        dest='quiet',
        action='store_true')
    parser.add_argument('--hard',
        help='Remove docker container and snapshot images.',
        dest='hard_reset',
        action='store_true')


def run_command(options):
    if not options.quiet:
        print("Resetting %s" % options.environment_path)

    if not os.path.exists(options.config_file):
        if not options.quiet:
            print("Environment does not exists - nothing to reset.")
        return

    config = Config(options.config_file)
    docker_client = docker.Client(version='auto')

    _remove_container(docker_client, config, options.quiet)
    if options.hard_reset:
        _remove_snapshots(docker_client, config, options.quiet)


def _remove_container(docker_client, config, quiet):
    container_id = config['global']['container_id']
    if container_id:
        docker_client.stop(container_id)
        if not quiet:
            print("  Removing container %s" % container_id)
        docker_client.remove_container(container_id)

    del config['global']['container_id']
    config.write()


def _remove_snapshots(docker_client, config, quiet):
    snapshots = config['global']['snapshots'] or ()
    for image_id in snapshots:
        if not quiet:
            print("  Removing image %s" % image_id)
        docker_client.remove_image(image_id)

    del config['global']['snapshots']
    config.write()
