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
