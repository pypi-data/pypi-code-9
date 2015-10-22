import io
import json
import logging
import re
import sys

import docker
try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess

from ..flock import UsageCounter
from ..config import Config
from .. import user, cli


NEEDS_ENVIRONMENT = True

_log = logging.getLogger(__name__)

_NOT_CREATED = 1
_NOT_RUNNING = 2
_RUNNING     = 3


class DockerError(Exception):
    pass


class ImageError(DockerError):
    pass


def add_command_line_arguments(parser, _environ):
    parser.add_argument('executable', nargs='+')


def _initial_dockerfile(config):
    run = []
    expanded = user.expand_user(config)
    username = expanded['name']
    base_image = config['global']['base']

    # create groups
    for group in expanded['groups']:
        cmd = 'groupadd -f --gid %(gid)d %(name)s' % group
        run.append(cmd)

    # create user if not already exists
    cmd = 'getent passwd %s >/dev/null || useradd -M -N' % username
    if expanded['system']:
        cmd += ' --system'
    if expanded['uid']:
        cmd += ' --uid %d' % expanded['uid']
    if expanded['groups']:
        gids = []
        for group in expanded['groups']:
            gids.append('%d' % group['gid'])
        cmd += ' -G %s' % (','.join(gids))
    cmd += ' %s' % expanded['name']
    run.append(cmd)

    # set sudo without password
    if expanded['sudo'] and username:
        cmd = "echo '%s ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers" % username
        run.append(cmd)

    base_image = config['global']['base']
    dockerfile = '''
        FROM %s
        RUN %s
    ''' % (base_image, ' && '.join(run))

    return dockerfile.encode('utf-8')


def _build_initial_docker_image(docker_client, config):
    image_id = None
    error = None
    dockerfile = io.BytesIO(_initial_dockerfile(config))

    for line in docker_client.build(fileobj=dockerfile, rm=True):
        data = json.loads(line)
        if data.get('stream'):
            stream = data['stream']
            _log.info(stream.rstrip())
            pattern = r'(?:--->|Successfully built)\s*([a-f0-9]{12,})\s*$'
            match = re.search(pattern, stream, re.DOTALL | re.IGNORECASE)
            if match:
                image_id = match.group(1)
        if data.get('status'):
            _log.info(data['status'].rstrip())
        if data.get('error'):
            error = data['error']
            _log.error(error.rstrip())

    if error:
        raise DockerError(error)

    if not image_id:
        raise DockerError('no container id found')

    return image_id


def _container_state(docker_client, container_id):
    if not container_id:
        return _NOT_CREATED

    try:
        state = docker_client.inspect_container(container_id)
    except docker.errors.NotFound:
        return _NOT_CREATED

    if state['State']['Running']:
        return _RUNNING

    return _NOT_RUNNING


def _image_exists(docker_client, image_id):
    if not image_id:
        return False

    try:
        docker_client.inspect_image(image_id)
    except docker.errors.NotFound:
        return False
    return True


def _create_container(docker_client, config):
    image = None
    kwargs = {}

    while not image and config['global']['snapshots']:
        candidate = config['global']['snapshots'][-1]
        if _image_exists(docker_client, candidate):
            image = candidate
        else:
            _log.info('removing snapshot %s from configuration: image not found',
                candidate)
            config['global']['snapshots'].pop()
            config.write()

    if not image:
        # no (valid) snapshots
        image = _build_initial_docker_image(docker_client, config)
        config['global']['snapshots'] = [image]
        config.write()

    if config['directory']:
        volumes = config['directory'].keys()
        binds = {}
        for key, value in config['directory'].items():
            if ':' in value:
                vol_bind, vol_mode = value.rsplit(':', 1)
                binds[key] = {'bind': vol_bind, 'mode': vol_mode}
            else:
                binds[key] = {'bind': value}

        host_config = docker.utils.create_host_config(binds=binds)
        kwargs['host_config'] = host_config
        kwargs['volumes'] = volumes

    username = user.username_from_config(config)
    container = docker_client.create_container(
        user=username,
        image=image,
        tty=True,
        command='/bin/bash',
        **kwargs)
    if container.get('Warnings'):
        _log.warn(container['Warnings'])
    return container['Id']


def _start_container(docker_client, container_id):
    docker_client.start(container_id)


def _stop_container(docker_client, container_id):
    docker_client.stop(container_id)


def _exec_container(docker_client, container_id, command):
    # stdin is not yet implemented in docker_client.exec_start, so we need
    # to use the docker command line client.
    exitcode = subprocess.call(
        ['docker', 'exec', '-it', container_id] + command)
    return exitcode


def _setup_container(counter, config, docker_client):
    with counter:
        # reload configuration as it may have been modified by concurrently
        # running _setup_container calls.
        config.reload()

        container_id = config['global']['container_id']

        value = counter.incr()

        if not container_id:
            _log.warn('reset usage counter')
            counter.reset()
            value = counter.incr()

        if value == 1:
            # create and start on first execution
            state = _container_state(docker_client, container_id)

            if state == _NOT_CREATED:
                del config['global']['container_id']
                config.write()

                container_id = _create_container(docker_client, config)

                config['global']['container_id'] = container_id
                config.write()

                state = _container_state(docker_client, container_id)

            assert container_id
            if state == _NOT_RUNNING:
                # created but stopped
                _log.debug('starting container %s', container_id)
                _start_container(docker_client, container_id)
                state = _container_state(docker_client, container_id)

            assert state == _RUNNING

        return container_id


def _teardown_container(counter, config, docker_client, container_id):
    config.reload()
    persistent = config['global']['persistent']

    with counter:
        value = counter.decr()

        if value == 0 and not persistent:
            # last exit
            _stop_container(docker_client, container_id)


def run_command(options):
    docker_client = docker.Client(version='auto')
    counter = UsageCounter(options.counter_file)
    config = Config(options.config_file)

    container_id = _setup_container(counter, config, docker_client)

    # counter may increase while running this process
    exitcode = -1
    try:
        exitcode = _exec_container(
            docker_client, container_id, options.executable)
    finally:
        _teardown_container(counter, config, docker_client, container_id)

    sys.exit(exitcode)


def main():
    module = sys.modules[__name__]
    cli.standalone_command_main(module)

