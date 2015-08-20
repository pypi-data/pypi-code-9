__author__ = 'Sinisa'

import os
import mock
import json
from nose.tools import nottest
from mock import mock_open
from sbg_cli.config import Config, load_config
from sbg_cli.sbg_docker.docker_client.client import create_docker_client, Docker
from sbg_cli.sbg_docker.docker_client.utils import DOCKER_CONFIG_FILENAME, \
    get_session, logout_docker_cfg, dockerize_username


TEST_ENV = {
    'SBG_CONFIG_FILE': 'external_config.json',
}

DEFAULT_CONFIG = {}


def test_create_client():
    cfg = Config({'version': '1.17', 'timeout': 120})
    with mock.patch('sys.platform', 'linux2'):
        cl = create_docker_client(cfg)
        assert 'http+unix://var/run/docker.sock' in cl.client.base_url
        assert isinstance(cl, Docker)
    with mock.patch('sys.platform', 'darwin'):
        cl = create_docker_client(cfg)
        print cl.client.base_url
        assert '192.168.59.103:2376' in cl.client.base_url
        assert isinstance(cl, Docker)


def test_override_config_env():
    read_data = '{"docker_client_timeout": 1200, "docker_registry": "test_repository"}'
    with mock.patch('os.environ', TEST_ENV):
        with mock.patch('os.path.exists', lambda x: True):
            with mock.patch('{}.open'.format('__builtin__'), mock_open(read_data=read_data), create=True) as m:
                cfg = load_config()
                m.assert_called_once_with('external_config.json', 'r')
                assert cfg.docker_client_timeout == 1200
                assert cfg.docker_registry == 'test_repository'


def test_override_config():
    read_data = '{"docker_client_timeout": 1200, "docker_registry": "test_repository"}'
    with mock.patch('os.environ', TEST_ENV):
        with mock.patch('os.path.exists', lambda x: True):
            with mock.patch('{}.open'.format('__builtin__'), mock_open(read_data=read_data), create=True) as m:
                cfg = load_config()
                m.assert_called_once_with('external_config.json', 'r')
                assert cfg.docker_client_timeout == 1200
                assert cfg.docker_registry == 'test_repository'



def test_get_session():
    read_data = '{"images.sbgenomics.com": {"email": null, "auth": "dXNlcm5hbWU6NjZjZmRkM2YtN2EyMC00NTYyLWI0NzktZGNhMTNhZDRkYjcy"}}'
    with mock.patch('{}.open'.format('__builtin__'), mock_open(read_data=read_data), create=True) as m:
        session = get_session('images.sbgenomics.com')
        m.assert_called_once_with(os.path.join(os.environ.get('HOME', '.'), DOCKER_CONFIG_FILENAME), 'r')
        assert session == '66cfdd3f-7a20-4562-b479-dca13ad4db72'
    with mock.patch('{}.open'.format('__builtin__'), mock_open(read_data=read_data), create=True) as m:
        session = get_session('non-existent')
        m.assert_called_once_with(os.path.join(os.environ.get('HOME', '.'), DOCKER_CONFIG_FILENAME), 'r')
        assert not session

@nottest
def test_logout():
    read_data = '{"images.sbgenomics.com": {"email": null, "auth": "dXNlcm5hbWU6NjZjZmRkM2YtN2EyMC00NTYyLWI0NzktZGNhMTNhZDRkYjcy"}}'
    with mock.patch('{}.open'.format('__builtin__'), mock_open(read_data=read_data), create=True) as m:
        logout_docker_cfg('images.sbgenomics.com')
        with open(os.path.join(os.environ.get('HOME', '.'), DOCKER_CONFIG_FILENAME), 'r') as f:
            cfg = json.load(f)
            assert not cfg.get("images.sbgenomics.com")


def test_push():
    cl = create_docker_client()
    cl.push_cl('images.sbgenomics.com/sinisa/lalala', 'latest')


def dockerize_test():
    test_repository = "user-name/bla:latest"
    repo = dockerize_username(test_repository)
    assert repo == "user_name/bla:latest"

