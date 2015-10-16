import unittest2 as unittest
from Products.CMFCore.utils import getToolByName
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone import api
from .utils import *

from edeposit.policy.testing import EDEPOSIT_POLICY_INTEGRATION_TESTING

class TestProducent(unittest.TestCase):
    
    layer = EDEPOSIT_POLICY_INTEGRATION_TESTING
    edepositGroups = [
        'Librarians',
        'Library Administrators',
        'Acquisitors',
        'Acquisition Administrators',
        'Producent Administrators',
        'Producent Contributors',
        'Producent Editors',
    ]
    
    @withPortal
    def test_producent_folder(self, portal):
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('edeposit.user.producentfolder', 'edlf1', title=u"E-Deposit Library Folder")

    @withPortal
    @withProducentFolder
    def test_producent(self, portal, producentFolder, **kwargs):
        setRoles(portal, TEST_USER_ID, ('Member','E-Deposit: Producent'))
        producentFolder.invokeFactory('edeposit.user.producent', 'producent', title=u"E-Deposit Producent")
        producent = producentFolder['producent']
        content = producent.keys()
        self.assertTrue('epublications' in content)
        self.assertTrue('eperiodicals' in content)
        self.assertTrue('books' in content)
        self.assertTrue('administrators' in content)
        self.assertTrue('editors' in content)


    @withPortal
    @withProducentFolder
    def test_producent_users(self, portal, producentFolder, **kwargs):
        setRoles(portal, TEST_USER_ID, ('Member','E-Deposit: Producent'))
        producentFolder.invokeFactory('edeposit.user.producent', 'producent', title=u"E-Deposit Producent")
        producent = producentFolder['producent']
        administrators = producent['administrators']
        administrators.invokeFactory('edeposit.user.producentadministrator','admin',title=u"Administrator")
        editors = producent['editors']
        editors.invokeFactory('edeposit.user.producenteditor','editor',title=u"Editor")

    # @withPortal
    # def test_edeposit_groups(self, portal):
    #     gtool = api.portal.get_tool('portal_groups')
    #     groups = gtool.listGroups()
    #     groupIds = [ gr.getGroupId() for gr in groups]
    #     #import sys,pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    #     self.assertFalse(frozenset(self.edepositGroups) - frozenset(groupIds),'all groups for E-Deposit are created: remains: %s' % (frozenset(self.edepositGroups) - frozenset(groupIds),))
    #     pass

    # @withPortal
    # @withProducent
    # def test_producent_workflow(self, portal, producent, **kwargs):
    #     setRoles(portal, TEST_USER_ID, ('Member','E-Deposit: Producent'))

    #     roles = frozenset(['Owner','Member','E-Deposit: Producent','Authenticated','E-Deposit: Assigned Producent'])
    #     self.assertTrue(frozenset(api.user.get_roles(username=TEST_USER_ID, obj=producent)) == roles,
    #                     'all important roles are set for producent folder')
    #     self.assertTrue(api.content.get_state(obj=producent) == 'registration', "producent is in registration state")
    #     permissions = getUserPermissions(portal, TEST_USER_ID, producent)
    #     epublications = producent['epublications']
    #     self.assertTrue(frozenset(api.user.get_roles(username=TEST_USER_ID, obj=epublications)) == roles,
    #                     'all important roles are set for epublications folder')
    #     rolesForAddEpublication = [ii['name'] for ii in producent.rolesOfPermission('E-Deposit: Add ePublication') if ii['selected']]
    #     self.assertTrue(api.content.get_state(obj=producent) == 'registration', "producent is in registration state")
    #     wft = api.portal.get_tool('portal_workflow')
    #     wf = frozenset(['edeposit_producent_workflow',])
    #     self.assertTrue(wf == frozenset(wft.getChainForPortalType('edeposit.user.producent')),'producent has proper workflow')
    #     self.assertTrue(wft.getChainForPortalType('edeposit.content.epublicationfolder') == (),'epublication folder has no workflow')
    #     stateDefinition= wft['edeposit_producent_workflow'].states['registration']
    #     epublications.invokeFactory('edeposit.content.epublication','epublication', title=u"epublication")
    #     pass
