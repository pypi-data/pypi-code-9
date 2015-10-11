from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IPartial
from ftw.jsondump.tests.base import FtwJsondumpTestCase
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
import json


class TestWorkflowPartial(FtwJsondumpTestCase):

    def setUp(self):
        portal = self.layer['portal']
        self.wftool = getToolByName(portal, 'portal_workflow')
        self.wftool.setChainForPortalTypes(('Folder',),
                                           ('simple_publication_workflow',))

        self.folder = create(Builder('folder'))
        self.wftool.doActionFor(self.folder, 'publish')
        self.wftool.doActionFor(self.folder, 'retract')

    def test_partial_data(self):
        partial = getMultiAdapter((self.folder, self.folder.REQUEST),
                                  IPartial,
                                  name="workflow")

        config = {}
        partial_data = partial(config)

        records = self.folder.workflow_history.data[
            'simple_publication_workflow']

        self.assertEquals(
            {'_workflow_chain': {'simple_publication_workflow': 'private'},
             '_workflow_history': {'simple_publication_workflow':
                                   [
                                       {'action': None,
                                        'actor': 'test_user_1_',
                                        'comments': '',
                                        'review_state': None,
                                        'time': str(records[0]['time'])},
                                       {'action': 'publish',
                                        'actor': 'test_user_1_',
                                        'comments': '',
                                        'review_state': 'publish',
                                        'time': str(records[1]['time'])},
                                       {'action': 'retract',
                                        'actor': 'test_user_1_',
                                        'comments': '',
                                        'review_state': 'retract',
                                        'time': str(records[2]['time'])}]}},
            partial_data)

    def test_partial_is_jsonseriazable(self):
        partial = getMultiAdapter((self.folder, self.folder.REQUEST),
                                  IPartial,
                                  name="workflow")

        config = {}
        partial_data = partial(config)
        self.assertEquals(json.loads(json.dumps(partial_data)), partial_data)

    def test_do_not_fail_if_content_has_no_workflow(self):
        self.wftool.setChainForPortalTypes(('Document',),
                                           ('None',))

        self.folder = create(Builder('document'))

        partial = getMultiAdapter((self.folder, self.folder.REQUEST),
                                  IPartial,
                                  name="workflow")

        config = {}
        partial_data = partial(config)

        self.assertEquals({'_workflow_chain': {}, '_workflow_history': {}},
                          partial_data)
