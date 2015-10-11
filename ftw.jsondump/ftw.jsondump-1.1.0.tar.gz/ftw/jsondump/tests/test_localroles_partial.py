from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IPartial
from ftw.jsondump.tests.base import FtwJsondumpTestCase
from zope.component import getMultiAdapter
import json


class TestLocalRolesPartial(FtwJsondumpTestCase):

    def setUp(self):
        self.folder = create(Builder('folder'))
        self.user = create(Builder('user')
                           .with_roles('Editor', 'Reader', on=self.folder))

    def test_partial_data(self):
        partial = getMultiAdapter((self.folder, self.folder.REQUEST),
                                  IPartial,
                                  name="localroles")

        config = {}
        partial_data = partial(config)
        self.assertEquals({'__ac_local_roles__':
                           {'test_user_1_': ['Owner'],
                            'john.doe': ['Editor', 'Reader']},
                           '__ac_local_roles_block__': False},
                          partial_data)

    def test_partial_is_jsonseriazable(self):
        partial = getMultiAdapter((self.folder, self.folder.REQUEST),
                                  IPartial,
                                  name="localroles")

        config = {}
        partial_data = partial(config)
        self.assertEquals(json.loads(json.dumps(partial_data)), partial_data)

    def test_blocked_local_roles(self):
        self.folder.__ac_local_roles_block__ = True
        partial = getMultiAdapter((self.folder, self.folder.REQUEST),
                                  IPartial,
                                  name="localroles")

        config = {}
        partial_data = partial(config)

        self.assertTrue(partial_data['__ac_local_roles_block__'])
