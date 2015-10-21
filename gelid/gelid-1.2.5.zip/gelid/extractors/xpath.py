# -*- coding: UTF-8 -*-
# lvjiyong on 2015/4/19.

# 部分代码参考与复制自 python-goose: https://github.com/grangier/python-goose

from lxml import etree
import six

from gelid.extractors.enums import ItemProp, Pack


class HtmlTree(object):
    def __init__(self, source, url=None):
        self.url = url
        self.stores = {Pack.html: etree.HTML(source, base_url=url)}

    @property
    def html(self):
        return self.stores.get(Pack.html)

    @property
    def author(self):
        """
        从itemprop获取作者名
        :return:
        """
        nodes = HtmlTree.item_prop(self.html, ItemProp.author.name)
        for node in nodes:
            name_nodes = HtmlTree.item_prop(node, ItemProp.name.name)
            if len(name_nodes) > 0:
                names = HtmlTree.texts(name_nodes[0])
                return u''.join([name.strip() for name in names if isinstance(name, six.string_types)])

    @staticmethod
    def item_prop(node, name):
        """
        从itemprop结构获取节点
        :param node:
        :param name:
        :return:
        """
        return HtmlTree.elements(node, attr=ItemProp.itemprop.name, value=name)

    @staticmethod
    def elements(node, tag=None, attr=None, value=None, child=False):
        """
        使用tag的attr属性值value获取节点
        :param node:原始节点数据
        :param tag:
        :param attr:
        :param value:
        :param child:
        :return:
        """
        ns = "http://exslt.org/regular-expressions"
        selector = 'descendant-or-self::%s' % (tag or '*')
        if attr and value:
            selector = '%s[re:test(@%s, "%s", "i")]' % (selector, attr, value)
        elems = node.xpath(selector, namespaces={"re": ns})
        if node in elems and (tag or child):
            elems.remove(node)
        return elems

    @staticmethod
    def texts(node):
        """
        获取节点内容
        :param node:
        :return:
        """
        return [i for i in node.itertext()]
