from cleanenv.cleanenv_inside.config import Config
import pytest


def _to_dict(config):
    out = {}
    for section, section_config in config.items():
        out[section] = {}
        for key in section_config.keys():
            value = section_config[key]
            original = section_config.get_config_value(key)
            out[section][key] = value, original
    return out


def test_load_config_missing_file(datadir):
    path = datadir.join('missing.conf').strpath
    with pytest.raises(IOError):
        Config(path)


@pytest.mark.parametrize('filename', [
    'valid.conf',
    'valid2.conf',
])
def test_load_config(datadir, filename):
    path = datadir.join(filename).strpath
    config = Config(path)
    assert isinstance(config, dict)


@pytest.mark.parametrize('filename', [
    'empty.conf',
    'empty_sections.conf',
    'invalid.conf',
])
def test_load_config_invalid(datadir, filename):
    path = datadir.join(filename).strpath
    with pytest.raises(ValueError):
        Config(path)


@pytest.mark.parametrize('filename', [
    'valid.conf',
    'valid2.conf',
])
def test_save(tmpdir, datadir, filename):
    path = datadir.join(filename)
    path2 = tmpdir.join(filename)
    path.copy(path2)

    expect = Config(path.strpath)

    config = Config(path2.strpath)
    assert config == expect

    config.write()
    config.reload()
    assert config == expect

    # change and check
    config['global']['foo'] = 1
    config.write()
    config.reload()

    assert config != expect

