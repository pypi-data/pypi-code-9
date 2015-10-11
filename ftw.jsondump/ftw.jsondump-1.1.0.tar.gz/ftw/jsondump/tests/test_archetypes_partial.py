from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IPartial
from ftw.jsondump.tests.base import FtwJsondumpTestCase
from zope.component import getMultiAdapter
import json


class TestArchetypePartial(FtwJsondumpTestCase):

    def setUp(self):
        self.document = create(Builder('document')
                               .titled("My document"))

    def test_partial_is_jsonseriazable(self):
        partial = getMultiAdapter((self.document, self.document.REQUEST),
                                  IPartial,
                                  name="fields")

        config = {}
        partial_data = partial(config)
        self.assertEquals(json.loads(json.dumps(partial_data)), partial_data)
