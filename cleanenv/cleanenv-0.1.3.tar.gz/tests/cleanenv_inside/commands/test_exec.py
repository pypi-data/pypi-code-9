import io
import json
import re

import docker
import pytest

from flexmock import flexmock
from cleanenv.cleanenv_inside import user, cli
from cleanenv.cleanenv_inside.commands import exec_
from cleanenv.cleanenv_inside.config import Config
from cleanenv.cleanenv_inside.flock import UsageCounter


_not_found_error = docker.errors.NotFound(None, flexmock(content=None))


@pytest.fixture(scope='function')
def counter(tmpdir):
    filename = tmpdir.join('usage.counter')
    return UsageCounter(filename.strpath)


@pytest.fixture(scope='function')
def config(tmpdir):
    filename = tmpdir.join('cleanenv.conf')
    filename.write('''
        [global]
        base = dabase
        user = 1000:usr
        ''')
    return Config(filename.strpath)


@pytest.fixture(scope='function')
def docker_client():
    return flexmock()


def test_get_plugin():
    plugin = cli._get_plugin(exec_)
    assert plugin


def test_add_command_line_arguments(parser, environ):
    exec_.add_command_line_arguments(parser, environ)


def test_initial_dockerfile():
    flexmock(user) \
        .should_receive('expand_user') \
        .and_return({
            'name': 'uname',
            'groups': [{'name': 'g1', 'gid': 8}],
            'system': True,
            'sudo': True,
            'uid': 1001})

    config = {
        'global': {
            'base': 'img'
        }
    }

    result = exec_._initial_dockerfile(config)
    assert re.search(br'FROM img.*RUN.*g1.*uname.*sudoers', result, re.DOTALL)


def test_build_initial_docker_image(tmpdir):
    docker_client = flexmock()
    docker_client \
        .should_receive('build') \
        .with_args(fileobj=io.BytesIO, rm=True) \
        .and_return([
            json.dumps({'stream': 'Successfully built 0123456789ab'}),
            json.dumps({'status': 'ok'})])

    flexmock(exec_).should_receive('_initial_dockerfile')

    exec_._build_initial_docker_image(docker_client, {})


@pytest.mark.parametrize('output', [
    {'error': 'yes, it failed.'},
    {'stream': 'good, but no container id'}
])
def test_build_initial_docker_image_error(tmpdir, output):
    docker_client = flexmock()
    docker_client \
        .should_receive('build') \
        .with_args(fileobj=io.BytesIO, rm=True) \
        .and_return([json.dumps(output)])

    flexmock(exec_).should_receive('_initial_dockerfile')

    with pytest.raises(exec_.DockerError):
        exec_._build_initial_docker_image(docker_client, {})


def test_container_state_no_container(docker_client):
    result = exec_._container_state(docker_client, None)
    assert result == exec_._NOT_CREATED



def test_container_state_invalid_container(docker_client):
    docker_client \
        .should_receive('inspect_container') \
        .with_args('abcd') \
        .and_raise(_not_found_error)

    result = exec_._container_state(docker_client, 'abcd')
    assert result == exec_._NOT_CREATED


@pytest.mark.parametrize('inspection, expect', [
    ({'State': {'Running': False}}, exec_._NOT_RUNNING),
    ({'State': {'Running': True}},  exec_._RUNNING),
])
def test_container_state_container_exists(docker_client, inspection, expect):
    docker_client \
        .should_receive('inspect_container') \
        .with_args('abcd') \
        .and_return(inspection)

    result = exec_._container_state(docker_client, 'abcd')
    assert result == expect


def test_image_exists_negative(docker_client):
    docker_client \
        .should_receive('inspect_image') \
        .with_args('img1') \
        .and_raise(_not_found_error)

    result = exec_._image_exists(docker_client, 'img1')
    assert result == False

    result = exec_._image_exists(docker_client, None)
    assert result == False


def test_image_exists_positive(docker_client):
    docker_client \
        .should_receive('inspect_image') \
        .with_args('img1') \
        .and_return({'State': None})

    result = exec_._image_exists(docker_client, 'img1')
    assert result == True


def test_create_container_with_snapshot(config, docker_client):
    config['global']['snapshots'] = ['img1', 'img2', 'img3']
    config.write()

    flexmock(exec_) \
        .should_receive('_image_exists') \
        .and_return(False) \
        .and_return(True)
    flexmock(docker_client) \
        .should_receive('create_container') \
        .with_args(
            user='usr',
            image='img2',
            tty=True,
            command='/bin/bash') \
        .and_return({'Id': 'abcd', 'Warnings': 'Recreated'})

    result = exec_._create_container(docker_client, config)

    assert result == 'abcd'
    config.reload()
    assert config['global']['snapshots'] == ['img1', 'img2']


def test_create_container_from_scratch(config, docker_client):
    flexmock(exec_) \
        .should_receive('_build_initial_docker_image') \
        .with_args(docker_client, config) \
        .and_return('img1')
    flexmock(docker_client) \
        .should_receive('create_container') \
        .with_args(
            user='usr',
            image='img1',
            tty=True,
            command='/bin/bash') \
        .and_return({'Id': 'abcd'})

    result = exec_._create_container(docker_client, config)

    assert result == 'abcd'
    config.reload()
    assert config['global']['snapshots'] == ['img1']


def test_setup_container_in_use(counter, config, docker_client):
    # concurrent instance already running
    with counter:
        counter.incr()

    config['global']['container_id'] = 'abcd'
    config.write()

    result = exec_._setup_container(counter, config, docker_client)
    assert result == 'abcd'

    with counter:
        assert counter._get_value() == 2


def test_setup_container_created_not_running(counter, config, docker_client):
    # 'docker create' was somewhen called
    config['global']['container_id'] = 'abcd'
    config.write()

    flexmock(exec_) \
        .should_receive('_container_state') \
        .with_args(docker_client, 'abcd') \
        .and_return(exec_._NOT_RUNNING) \
        .and_return(exec_._RUNNING)

    docker_client.should_receive('start').once()

    result = exec_._setup_container(counter, config, docker_client)
    assert result == 'abcd'


def test_setup_container_first_time(counter, config, docker_client):
    # like in a fresh environment
    flexmock(exec_) \
        .should_receive('_container_state') \
        .and_return(exec_._NOT_CREATED) \
        .and_return(exec_._NOT_RUNNING) \
        .and_return(exec_._RUNNING)

    flexmock(exec_) \
        .should_receive('_create_container') \
        .and_return('abcd')

    docker_client.should_receive('start').once()

    result = exec_._setup_container(counter, config, docker_client)
    assert result == 'abcd'

    config.reload()
    assert config['global']['container_id'] == 'abcd'


def test_teardown_in_use(counter, config, docker_client):
    with counter:
        counter.incr()
        counter.incr()

    config['global']['container_id'] = 'abcd'
    config.write()

    exec_._teardown_container(counter, config, docker_client, 'abcd')

    with counter:
        assert counter._get_value() == 1
    config.reload()
    assert config['global']['container_id'] == 'abcd'


def test_teardown_persistent(counter, config, docker_client):
    with counter:
        counter.incr()

    config['global']['persistent'] = True
    config['global']['container_id'] = 'abcd'
    config.write()

    exec_._teardown_container(counter, config, docker_client, 'abcd')

    with counter:
        assert counter._get_value() == 0
    config.reload()
    assert config['global']['container_id'] == 'abcd'


def test_teardown_last(counter, config, docker_client):
    with counter:
        counter.incr()

    config['global']['container_id'] = 'abcd'
    config.write()

    flexmock(docker_client) \
        .should_receive('stop') \
        .with_args('abcd')

    exec_._teardown_container(counter, config, docker_client, 'abcd')

    with counter:
        assert counter._get_value() == 0
    config.reload()
    assert config['global']['container_id'] == 'abcd'


def test_run_command(tmpdir, docker_client):
    config_file = tmpdir.join('cleanenv.conf')
    config_file.write('''
        [global]
        base = dabase
        user = 1000:usr
        ''')

    options = flexmock(
        config_file=config_file.strpath,
        counter_file=tmpdir.join('usage.counter').strpath,
        executable=['some-binary', '--with', '--args'])

    flexmock(docker) \
        .should_receive('Client') \
        .and_return(docker_client)
    flexmock(exec_) \
        .should_receive('_setup_container') \
        .and_return('abcd')
    flexmock(exec_).should_receive('_teardown_container')
    flexmock(exec_.subprocess) \
        .should_receive('call') \
        .with_args(
            ['docker', 'exec', '-it', 'abcd',
             'some-binary', '--with', '--args']) \
        .and_return(0)

    with pytest.raises(SystemExit):
        exec_.run_command(options)


def test_main():
    flexmock(cli) \
        .should_receive('standalone_command_main') \
        .with_args(exec_)
    exec_.main()
