import os
from flexmock import flexmock
from cleanenv.commands import create

import pytest


def test_add_command_line_arguments(parser, environ):
    flexmock(os, getlogin='tester', getuid=1234)
    create.add_command_line_arguments(parser, environ)


@pytest.mark.slow
def test_run_command(tmpdir):
    dest_dir = tmpdir.join('env')

    options = flexmock(
        base_image='test',
        config_file=None,
        dest_dir=dest_dir.strpath,
        directory=[],
        generate_config=False,
        link=[],
        on_activate=[],
        persistent=False,
        sudo=False,
        user=None)

    create.run_command(options)

    assert dest_dir.join('cleanenv.conf').exists()
    assert dest_dir.join('.env').exists()
    assert dest_dir.join('bin').exists()
    assert dest_dir.join('bin').join('activate').exists()
