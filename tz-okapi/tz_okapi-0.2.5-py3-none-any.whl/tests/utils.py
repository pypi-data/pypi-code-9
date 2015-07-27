import json
import unittest

from okapi.core.loggers.tests import TestLogger
from okapi.rst.directives import load_directives
from okapi.settings import settings


class TestCase(unittest.TestCase):
    def setUp(self):
        load_directives()
        settings.headers.visible = {}
        settings.headers.hidden = {}
        settings.log = TestLogger()
        settings.log.verbosity = 99
        settings.cache.storage = {}
        return super(TestCase, self).setUp()


class TestResponse(object):
    def __init__(self, **kwargs):
        self.content = ''
        self.headers = {}
        self.status_code = 200

        self.__dict__.update(kwargs)

    def json(self):
        return json.loads(self.content)

    @property
    def text(self):
        return self.content
