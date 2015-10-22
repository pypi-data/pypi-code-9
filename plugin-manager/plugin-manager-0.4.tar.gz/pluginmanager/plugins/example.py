# -*- coding: utf-8 -*-


class Example(object):
    """
    这是一个插件的例子，如果需要会自动扫描，必须配置plugin_info信息
    """
    plugin_info = {'name': 'example', 'cls': 'pluginmanager.plugins.example.Example', 'author': 'lvjiyong',
                   'description': u'这是一个示例'}

    def hello(self, name):
        return 'hello %s' % name