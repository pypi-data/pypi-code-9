import os

import pytest
from flexmock import flexmock

from cleanenv.cleanenv_inside import cli
from cleanenv.cleanenv_inside.commands import link


def test_get_plugin():
    plugin = cli._get_plugin(link)
    assert plugin


def test_add_command_line_arguments(parser, environ):
    link.add_command_line_arguments(parser, environ)


def test_run_command(tmpdir):
    options = flexmock(
        bin_dir=tmpdir.strpath,
        dest='an_exe',
        source='/bin/egg')
    link.run_command(options)

    dest = tmpdir.join('an_exe')
    assert dest.exists()
    mode = os.stat(dest.strpath).st_mode & 0o777
    assert mode == 0o755
    binary = dest.read_binary()
    assert b'exec $CLEAN_ENV/.env/bin/inenv -- /bin/egg $@' in binary


@pytest.mark.parametrize('dest', [
    '../is-relative',
    '/is/absolute'
])
def test_run_command_error(dest):
    options = flexmock(
        bin_dir=None,
        source=None,
        dest=dest)
    with pytest.raises(Exception):
        link.run_command(options)


def test_install_program_links():
    link_mock = flexmock(link)
    link_mock \
        .should_receive('install_program_link') \
        .with_args('bin-dir', 'from', 'to')

    config = {
        'link': {
            'from': 'to'}}

    link.install_program_links('bin-dir', config)

