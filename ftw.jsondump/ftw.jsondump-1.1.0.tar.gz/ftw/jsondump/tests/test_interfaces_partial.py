from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IPartial
from ftw.jsondump.tests.base import FtwJsondumpTestCase
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.interface import Interface
import json


class IDummyInterface(Interface):

    """Dummy marker interface"""


class TestInterfacesPartial(FtwJsondumpTestCase):

    def test_interfaces_partial(self):
        document = create(Builder('document').titled('A Title'))

        alsoProvides(document, IDummyInterface)

        partial = getMultiAdapter((document, document.REQUEST), IPartial,
                                  name="interfaces")

        config = {}
        data = partial(config)

        self.assertEquals(
            {'_directly_provided':
             ['Products.CMFEditions.interfaces.IVersioned',
              'ftw.jsondump.tests.test_interfaces_partial.IDummyInterface']},
            data)

        self.assert_structure_equal(json.loads(json.dumps(data)), data)
