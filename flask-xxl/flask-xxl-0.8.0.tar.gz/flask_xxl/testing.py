# -*- coding: utf-8 -*-
"""
    testing.py
    ~~~~~~~
    TestCase for testing
    :license: BSD3
"""
from flask.ext.testing import TestCase
from .main import AppFactory
from .basemodels import BaseMixin as BaseModel
from sqlalchemy import create_engine
from test_settings import BaseConfig as TestingConfig
import os

print os.getcwd()

meta = BaseModel.metadata
TEST_DB = 'sqlite:///:memory:'

class BaseTestCase(TestCase):

    def create_app(self):
        app = AppFactory(TestingConfig).get_app(__name__)
        return app
        

    def setUp(self):
        self.app = self.create_app()
        self.db = BaseModel
        self.db._engine = create_engine(TEST_DB)
        self.db._engine.echo = True
        meta.bind = self.db._engine
        meta.drop_all()
        meta.create_all()

    def tearDown(self):
        self.db.session.close()
        meta.drop_all()


    def assertContains(self, response, text, count=None,
                       status_code=200, msg_prefix=''):
        """
        Asserts that a response indicates that some content was retrieved
        successfully, (i.e., the HTTP status code was as expected), and that
        ``text`` occurs ``count`` times in the content of the response.
        If ``count`` is None, the count doesn't matter - the assertion is true
        if the text occurs at least once in the response.
        """

        if msg_prefix:
            msg_prefix += ": "

        self.assertEqual(response.status_code, status_code,
            msg_prefix + "Couldn't retrieve content: Response code was %d"
                         " (expected %d)" % (response.status_code, status_code))

        real_count = response.data.count(text)
        if count is not None:
            self.assertEqual(real_count, count,
                msg_prefix + "Found %d instances of '%s' in response"
                             " (expected %d)" % (real_count, text, count))
        else:
            self.assertTrue(real_count != 0,
                    msg_prefix + "Couldn't find '%s' in response" % text)
