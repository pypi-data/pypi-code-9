import os.path
# from sys import version_info
# if version_info[0] == 2:
#     from mock import patch, mock_open, call
# else:
#     from unittest.mock import patch, mock_open, call

from pytest import fail
from py.path import local
from click.testing import CliRunner

import envtool


def _fixture(name):
    return os.path.join(os.path.dirname(__file__), 'fixtures', name)


def test_envfile_to_dict():
    assert envtool.envfile_to_dict(_fixture('basic_envfile')) == {'A': 'abcde', 'B': 'def'}


def test_parse_envfile_contents():
    assert envtool.parse_envfile_contents("""
        # Comment
        a=b
        """) == {'a': 'b'}


def test_parse_invalid_envfile_contents():
    try:
        envtool.parse_envfile_contents("""
a
        """)
        fail()
    except IOError:
        assert True


def test_envdir_to_dict():
    res = envtool.envdir_to_dict(_fixture('basic_envdir'))
    assert res == {'A': 'abcde', 'B': 'def'}


def test_dict_to_envdir(tmpdir):
    output = tmpdir.join('saved_envdir')
    envtool.dict_to_envdir({'A': 'secret', 'B': 'plethora'}, str(output))
    assert output.join('A').read() == 'secret'
    assert output.join('B').read() == 'plethora'


def test_dict_to_envdir_preexisting(tmpdir):
    output = tmpdir.join('saved_envdir')
    output.mkdir()
    envtool.dict_to_envdir({'A': 'secret', 'B': 'plethora'}, str(output))
    assert output.join('A').read() == 'secret'
    assert output.join('B').read() == 'plethora'


def test_dict_to_envfile(tmpdir):
    output = tmpdir.join('saved_envfile')
    envtool.dict_to_envfile({'A': 'secret', 'B': 'plethora'}, str(output))
    assert output.read() == """A=secret
B=plethora
"""


def test_convert_to_envfile(tmpdir):
    output = tmpdir.join('converted_envfile')
    envtool.convert_to_envfile(_fixture('basic_envdir'), str(output))
    assert output.read() == """A=abcde
B=def
"""


def test_convert_to_envdir(tmpdir):
    output = tmpdir.join('converted_envdir')
    envtool.convert_to_envdir(_fixture('basic_envfile'), str(output))
    assert output.join('A').read() == 'abcde'
    assert output.join('B').read() == 'def'


def test_parse_missing_file(tmpdir):
    output = tmpdir.join('non-existent')
    assert not output.check()
    try:
        envtool.parse_env(str(output))
        assert False, "Parsing a missing env should fail with IOError"
    except IOError:
        assert True


def test_cli_envdir():
    runner = CliRunner()
    with runner.isolated_filesystem():
        output = local('cli_output')
        result = runner.invoke(envtool.main, ['convert', _fixture('basic_envfile'), str('cli_output')])
        assert result.exit_code == 0
        assert output.join('A').read() == 'abcde'
        assert output.join('B').read() == 'def'


def test_cli_envfile():
    runner = CliRunner()
    with runner.isolated_filesystem():
        output = local('cli_output')
        result = runner.invoke(envtool.main, ['convert', _fixture('basic_envdir'), str('cli_output')])
        assert result.exit_code == 0
        assert output.read() == """A=abcde
B=def
"""


def test_cli_missing_source():
    runner = CliRunner()
    with runner.isolated_filesystem():
        non_existent = local('non-existent')
        assert not non_existent.check()
        result = runner.invoke(envtool.main, ['convert', str(non_existent), 'cli_output'])
        assert result.exit_code == 2


def test_cli_incorrect_param():
    runner = CliRunner()
    with runner.isolated_filesystem():
        src = local('src')
        dest = local('dest')
        src.mkdir()
        dest.mkdir()
        result = runner.invoke(envtool.main, ['convert', str(src), str(dest)])
        assert result.exit_code == -1


if __name__ == '__main__':
    pytest.main()
