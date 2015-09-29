from __future__ import absolute_import
from click.testing import CliRunner
from precs.precs import cli


def test__cli_help_successful():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert 'fromkv' in result.output
    assert result.exit_code == 0


def test__fromkv_help_successful():
    runner = CliRunner()
    result = runner.invoke(cli, ['fromkv', '--help'])
    assert '-r, --record-delim TEXT  Delimiter separating records. Default: "END\\n".' in result.output
    assert '-e, --entry-delim TEXT   Delimiter separating entries. Default: "\\n".' in result.output
    assert '-f, --field-delim TEXT   Delimiter separating key-value fields.' in result.output
    assert '--help                   Show this message and exit.' in result.output
    assert result.exit_code == 0


def test__fromkv_defaults():
    runner = CliRunner()
    from tests.kv_testdata import INPUT1, OUTPUT1
    result = runner.invoke(cli, ['fromkv'], input=INPUT1)
    assert result.exit_code == 0
    assert OUTPUT1 == result.output


def test__fromkv_custom_delimiters2():
    runner = CliRunner()
    from tests.kv_testdata import INPUT2, OUTPUT2
    result = runner.invoke(cli, ['fromkv', '--field-delim', '=', '--record-delim', '%\n'], input=INPUT2)
    assert result.exit_code == 0
    assert OUTPUT2 == result.output


def test__fromkv_custom_delimiters3():
    runner = CliRunner()
    from tests.kv_testdata import INPUT3, OUTPUT3
    result = runner.invoke(cli, ['fromkv',
                                 '--field-delim', '=',
                                 '--entry-delim', '|',
                                 '--record-delim', '%\n'],
                           input=INPUT3)
    assert result.exit_code == 0
    assert OUTPUT3 == result.output


def test__fromkv_custom_delimiters4():
    runner = CliRunner()
    from tests.kv_testdata import INPUT4, OUTPUT4
    result = runner.invoke(cli, ['fromkv',
                                 '--field-delim', '=',
                                 '--entry-delim', '|',
                                 '--record-delim', '%'],
                           input=INPUT4)
    assert result.exit_code == 0
    assert OUTPUT4 == result.output



