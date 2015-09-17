# -*- coding: utf-8 -*-

"""
Plugin 基本信息
"""
from debuglog import logger

from parameter import Parameter

__all__ = ['Plugin']
_PLUGINS_CLAZZ_CACHE = {}


def get_clazz(cls_path):
    """
    获取
    :param cls_path:
    :return:

    >>> get_clazz(None)

    >>> get_clazz('pluginmanager.core.plugin.Plugin')
    <class 'pluginmanager.core.plugin.Plugin'>
    """

    if cls_path:
        pos = cls_path.rfind('.')
        package = cls_path[:pos]
        name = cls_path[pos + 1:]
        module = __import__(package, globals(), locals(), name, -1)
        return getattr(module, name)


class Plugin(Parameter):
    """
    域名相关配置信息

    >>> access = Plugin(name='test',cls='test')
    >>> getattr(access, 'name')
    'test'
    >>> access.args
    {}

    >>> plugin_dict =   {'description': u'\u8fd9\u662f\u4e00\u4e2a\u793a\u4f8b', 'author': 'lvjiyong', 'support_url': None, 'args': {}, 'enabled': 1, 'setting_cls': None, 'version': 1.0, 'setting_url': u'/plugins/setting/\u63d2\u4ef6\u4f8b\u5b50', 'cls': 'pluginmanager.plugins.example.Example', 'about_url': u'/plugins/about/\u63d2\u4ef6\u4f8b\u5b50', 'name': u'\u63d2\u4ef6\u4f8b\u5b50'}
    >>> plugin = Plugin(**plugin_dict)
    >>> plugin.cls
    'pluginmanager.plugins.example.Example'
    >>> plugin.clazz()
    <class 'pluginmanager.plugins.example.Example'>
    >>> plugin.clazz()
    <class 'pluginmanager.plugins.example.Example'>
    >>> plugin.doc()
    u'\\n    \u8fd9\u662f\u4e00\u4e2a\u63d2\u4ef6\u7684\u4f8b\u5b50\uff0c\u5982\u679c\u9700\u8981\u4f1a\u81ea\u52a8\u626b\u63cf\uff0c\u5fc5\u987b\u914d\u7f6eplugin_info\u4fe1\u606f\\n    '
    >>> example = plugin.clazz()()
    >>> example.hello('world!')
    'hello world!'

    """

    def __init__(self, **kwargs):
        # plugin name
        self.name = None
        # plugin class
        self.cls = None
        # 描述
        self.description = None
        # version
        self.version = 1.0

        # author
        self.author = None
        # support url
        self.support_url = None
        self.about_url = None
        self.setting_url = None
        # args note
        self.args = {}
        # 默认启用
        self.enabled = 1
        super(Plugin, self).__init__(**kwargs)

        if not self.cls:
            raise IndexError(u"plugin必须有cls数据")

        if not self.name:
            self.name = self._clazz_name().lower()

        if not self.about_url:
            self.about_url = '/plugins/about/%s' % self._clazz_name().lower()
        if not self.setting_url:
            self.setting_url = '/plugins/setting/%s' % self._clazz_name().lower()

    def _module_name(self):
        """
        对象模块名
        :return:
        """
        return self.cls[:self.cls.rfind('.')]

    def _clazz_name(self):
        """
        对象名
        :return:
        """
        return self.cls[self.cls.rfind('.') + 1:]

    def _module(self):
        _name = self._clazz_name()
        _module = self._module_name()
        return __import__(_module, globals(), locals(), _name, -1)

    def clazz(self):
        """
        获取plugin的class对象
        :return:
        """
        global _PLUGINS_CLAZZ_CACHE
        _clazz = _PLUGINS_CLAZZ_CACHE.get(self.cls)
        if not _clazz:
            _name = self._clazz_name()
            module = self._module()
            _clazz = getattr(module, _name)
            _PLUGINS_CLAZZ_CACHE[self.cls] = _clazz

        return _clazz

    def _file(self):
        return self._module().__file__[:-1]

    def code(self):
        with open(self._file(), 'r') as f:
            data = f.read()
        return data

    def remove_cache(self):
        """
        清除缓存的class对象
        :return:
        """
        global _PLUGINS_CLAZZ_CACHE
        if self.cls in _PLUGINS_CLAZZ_CACHE:
            del _PLUGINS_CLAZZ_CACHE[self.cls]

    def doc(self):
        """
        对象说明
        :return:
        """
        return self.clazz().__doc__.decode()


if __name__ == "__main__":
    import doctest

    doctest.testmod()