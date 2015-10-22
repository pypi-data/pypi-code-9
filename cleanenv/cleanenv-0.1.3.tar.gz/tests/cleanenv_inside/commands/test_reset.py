import docker
from flexmock import flexmock

from cleanenv.cleanenv_inside import cli
from cleanenv.cleanenv_inside.commands import reset
from cleanenv.cleanenv_inside.config import Config


def test_get_plugin():
    plugin = cli._get_plugin(reset)
    assert plugin


def test_run_command(tmpdir):
    sample_config = tmpdir.join('cleanenv.conf')
    sample_config.write('''
        [global]
        base = ignored
        container_id = abcdef
        snapshots = ghijkl, mnopq''')

    options = flexmock(
        quiet=False,
        hard_reset=True,
        environment_path=tmpdir.strpath,
        config_file=sample_config.strpath)

    client = flexmock()
    flexmock(docker) \
        .should_receive('Client') \
        .and_return(client)
    client.should_receive('stop').with_args('abcdef')
    client.should_receive('remove_container').with_args('abcdef')
    client.should_receive('remove_image').with_args('ghijkl')
    client.should_receive('remove_image').with_args('mnopq')

    reset.run_command(options)

    # verify
    config = Config(sample_config.strpath)
    assert config['global']['base'] == 'ignored'
    assert not config['global']['container_id']
    assert not config['global']['snapshots']
