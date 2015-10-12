# -*- coding: utf-8 -*-
import codecs

from cghq_common import config

CONFIG_FILE = 'tests/fixtures/test_config.yaml'


def test_load():
    # test without defaults
    with codecs.open(CONFIG_FILE, 'r') as handle:
        conf = config.load(handle)

    assert conf['key'] == 'value'
    assert conf['another_key'] == 123


def test_load_with_defaults():
    defaults = {'key': 'another_value', 'missing': 'default'}
    with codecs.open(CONFIG_FILE, 'r') as handle:
        conf = config.load(handle, defaults=defaults)

    assert conf['key'] == 'value'
    assert conf['another_key'] == 123
    assert conf['missing'] == 'default'


def test_save(tmpdir):
    conf_obj = {'name': 'P.T. Anderson'}
    outfile = tmpdir.join('some_config.yaml')
    config.save(conf_obj, outfile)

    assert outfile.exists()
    assert outfile.read() == "{name: P.T. Anderson}\n"
