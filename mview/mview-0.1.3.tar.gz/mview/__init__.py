__author__ = 'Zhichao HAN'


import os
import codecs
import collections
import ConfigParser


from tool import show_by_tool as show


config = collections.defaultdict(str)

_path_config = os.path.expanduser('~/.mview.cfg')


def init_pacakge(path_config=_path_config):
    cfg = ConfigParser.RawConfigParser()
    cfg.read(path_config)
    for k, v in cfg.items('MView'):
        config[k] = v


def update_executor(path, path_config=_path_config):
    cfg = ConfigParser.RawConfigParser()
    cfg.read(path_config)
    cfg.set('MView', 'executor', path)
    with codecs.open(path_config, 'w+', 'utf-8') as fp:
        cfg.write(fp)
    _auto_init_package()


def dump_package(config=collections.defaultdict(str), path=_path_config):
    raw = ConfigParser.RawConfigParser()
    raw.add_section('MView')
    for k, v in config.items():
        raw.set('MView', k, v)
    with codecs.open(_path_config, 'w+', 'utf-8') as fp:
        raw.write(fp)


def _auto_init_package():
    if not os.path.exists(_path_config):
        dump_package()
    init_pacakge(_path_config)

_auto_init_package()
