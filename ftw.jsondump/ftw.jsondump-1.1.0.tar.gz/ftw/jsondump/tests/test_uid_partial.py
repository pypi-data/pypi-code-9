from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IPartial
from ftw.jsondump.tests.base import FtwJsondumpTestCase
from zope.component import getMultiAdapter
import json


class TestUIDPartial(FtwJsondumpTestCase):

    def test_uuid_partial(self):
        document = create(Builder('document'))

        partial = getMultiAdapter((document, document.REQUEST), IPartial,
                                  name="uid")
        data = partial({})
        self.assertEquals({'_uid': document.UID()}, data)
        self.assert_structure_equal(json.loads(json.dumps(data)), data)
