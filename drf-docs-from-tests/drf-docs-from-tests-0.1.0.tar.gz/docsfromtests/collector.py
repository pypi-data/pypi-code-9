# -*- coding: utf-8 -*-

import os
import json
import codecs

from collections import defaultdict
from django.template.loader import render_to_string
from . import conf


def json_pretty_print(data):
    if not data:
        return u''

    if isinstance(data, (dict, list)):
        return json.dumps(data, sort_keys=True,
                          indent=4, separators=(',', ': '))

    try:
        return json.dumps(json.loads(data), sort_keys=True,
                          indent=4, separators=(',', ': '))

    except ValueError:
        return u''


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class DocCollector(Singleton):
    _data = defaultdict(lambda: defaultdict(lambda: []))

    def add(self, testcase, text):
        self._data[testcase.__class__][testcase._testMethodName].append(text)

    def _make_name(self, testcase_class, file_format=conf.FILE_FORMAT):
        return u'{}_{}.{}'.format(
            testcase_class.__module__.replace('.', '_'),
            testcase_class.__name__, file_format)

    def render_to_file(self, testcase_class):
        name = self._make_name(testcase_class)
        path = os.path.join(conf.DOCS_PATH, name)

        context = {
            'this': self,
            'file_name': name,
            'caption': testcase_class.caption,
            'description': testcase_class.description,
            'testcase_class': testcase_class,
            'data': dict(self._data[testcase_class]),
        }

        with codecs.open(path, 'w', encoding="utf-8") as f:
            f.write(render_to_string(conf.BASE_TEMPLATE, context))

    def render(self):
        for testcase_class in self._data:
            self.render_to_file(testcase_class)
