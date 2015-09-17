# -*- coding: utf-8 -*-

"""
PLUGIN 配置加载
"""

import json
import os
from plugin import Plugin
from debuglog import logger


def update_plugin(plugin_dict, plugins=None):
    """
    更新插件
    :param plugin_dict:
    :param plugins:
    :return:

    >>> data = {'test1': {'name':'Test1', 'cls':'cls1', 'author':'lvjiyong','description':'description1'},'test2': {'name':'test2', 'cls':'cls2'}}
    >>> data
    {'test1': {'description': 'description1', 'author': 'lvjiyong', 'name': 'Test1', 'cls': 'cls1'}, 'test2': {'name': 'test2', 'cls': 'cls2'}}
    >>> jd = update_plugin(data)
    >>> jd['test1']['name']
    'Test1'
    >>> jd['test1']['about_url']
    '/plugins/about/cls1'
    >>> jd['test1']['author']
    'lvjiyong'
    >>> data = {'test1': {'name':'test1', 'cls':'cls1', 'author':'lvjiyong1'},'test2': {'name':'test2', 'cls':'cls2','author':'lvjiyong'}}
    >>> jd2 = update_plugin(data, jd)
    >>> jd2['test1']['author']
    'lvjiyong1'
    >>> jd2['test1']['description']
    'description1'
    >>> jd2['test2']['author']
    'lvjiyong'
    """

    if plugin_dict:
        assert plugin_dict, u'data必须是dict序列化数据，请参考说明文档'

    if not plugins:
        plugins = {}

    for k, v in plugin_dict.iteritems():

        k = k.lower()
        if v:
            # logger.debug(k)
            plugin = Plugin(**v)
            # logger.debug('plugins:{}'.format(plugins))
            old_plugin = plugins.get(k)
            # logger.debug('old_plugin:%s' % old_plugin)
            if not old_plugin:
                plugins[k] = plugin
                # logger.debug(plugins)
            else:
                for pk, pv in plugin.iteritems():
                    if pv or pk not in old_plugin:
                        old_plugin[pk] = pv
        else:
            logger.warn(u'%s定义了plugin标识但却无plugin信息' % k)

    return plugins


def load_json(data, plugins=None):
    """
    从json数据中加载
    :param data:
    :return:

    >>> data = json.dumps({'test1': {'name':'test1', 'cls':'cls1'},'test2': {'name':'test2', 'cls':'cls2'}})
    >>> data
    '{"test1": {"name": "test1", "cls": "cls1"}, "test2": {"name": "test2", "cls": "cls2"}}'
    >>> jd = load_json(data)
    >>> str(jd['test1']['name'])
    'test1'
    >>> str(jd['test1']['about_url'])
    '/plugins/about/cls1'

    """

    json_data = json.loads(data)
    return update_plugin(json_data, plugins)


def load_json_file(f, plugins=None):
    """
    从json文件中加载数据
    :param f:
    :return:
    >>> f = '../../tests/data/plugins.json'
    >>> data = load_json_file(f)
    >>> str(data['test1']['name'])
    'test1'

    """
    json_data = json.load(file(f))
    return update_plugin(json_data, plugins)



def load_py(py, plugins=None):
    """
    从python文件中获取
    :param py:
    :return:

    >>> plugins = load_py('../plugins/example.py')
    >>> plugins
    {'example': {'description': u'\u8fd9\u662f\u4e00\u4e2a\u793a\u4f8b', 'author': 'lvjiyong', 'support_url': None, 'args': {}, 'enabled': 1, 'version': 1.0, 'setting_url': '/plugins/setting/example', 'cls': 'pluginmanager.plugins.example.Example', 'about_url': '/plugins/about/example', 'name': 'example'}}
    """
    try:
        context = {}
        with open(py) as fd:
            exec (fd.read(), context)
        for name, clazz in context.items():
            if hasattr(clazz, 'plugin_info'):
                plugins = update_plugin({clazz.__name__: clazz.plugin_info}, plugins)
    except:
        logger.warn('Error loading file %s. Ignored' % py)

    return plugins


def load_dir(dp, plugins=None):
    """
    从文件夹中读取
    :param dp:
    :return:

    >>> plugins = load_dir('../plugins')
    >>> plugins
    {'example': {'description': u'\u8fd9\u662f\u4e00\u4e2a\u793a\u4f8b', 'author': 'lvjiyong', 'support_url': None, 'args': {}, 'enabled': 1, 'version': 1.0, 'setting_url': '/plugins/setting/example', 'cls': 'pluginmanager.plugins.example.Example', 'about_url': '/plugins/about/example', 'name': 'example'}}

    """

    files = os.listdir(dp)
    for f in files:
        f = os.path.join(dp, f)
        logger.debug(f)
        logger.debug(os.path.isfile(f))
        if os.path.isfile(f) and f.endswith('.py'):
            plugins = load_py(f, plugins)
        elif os.path.isdir(f):
            plugins = load_dir(f, plugins)
    return plugins


if __name__ == "__main__":
    import doctest

    doctest.testmod()