import pytest
from spex.runner import spex


def test_fail_mode(mocker):
    mocker.patch('spex.args.parse_commandline', return_value=dict(mode='broken'))
    with pytest.raises(SystemExit) as sys_exit:
        spex()
