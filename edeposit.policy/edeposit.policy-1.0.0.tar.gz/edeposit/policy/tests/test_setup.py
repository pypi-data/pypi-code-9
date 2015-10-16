import unittest2 as unittest
from Products.CMFCore.utils import getToolByName

from edeposit.policy.testing import EDEPOSIT_POLICY_INTEGRATION_TESTING

from .utils import *

def installedTypesTestFactory(*types):
    def test(self):
        portal = self.layer['portal']
        portal_types = getToolByName(portal, 'portal_types')
        for checked_type in types:
            self.assertTrue(checked_type in portal_types, "%s installed" % (checked_type,))
    return test

def installedWorkflowsTestFactory(*workflows):
    def test(self):
        portal = self.layer['portal']
        workflow = getToolByName(portal, 'portal_workflow')
        wfIds =  workflow.getWorkflowIds()
        for wf in workflows:
            self.assertTrue(wf in wfIds, "%s installed" % (wf,))
    return test

class TestSetup(unittest.TestCase):
    
    layer = EDEPOSIT_POLICY_INTEGRATION_TESTING
    
    test_edeposit_types_installed = installedTypesTestFactory('edeposit.content.epublication',
                                                              'edeposit.content.epublicationfolder',
                                                              'edeposit.user.producent',
                                                              'edeposit.user.producentfolder',
                                                              'edeposit.user.producentadministrator',
                                                              'edeposit.user.producentadministratorfolder',
                                                              'edeposit.user.producenteditor',
                                                              'edeposit.user.producenteditorfolder',
                                                              'edeposit.content.book',
                                                              'edeposit.content.bookfolder',
                                                              )

    test_edeposit_workflows_installed = installedWorkflowsTestFactory('edeposit_producent_workflow',
                                                                      'edeposit_epublication_workflow',
                                                                      'edeposit_producentfolder_workflow',
                                                                      'edeposit_eperiodical_workflow',
                                                                      )

    # def test_portal_title(self):
    #     portal = self.layer['portal']
    #     self.assertEqual("E-Deposit Site", portal.getProperty('title'), 'portal title')
    
    # def test_portal_description(self):
    #     portal = self.layer['portal']
    #     self.assertEqual("Welcome to E-Deposit", portal.getProperty('description'))
    
    # def test_role_added(self):
    #     portal = self.layer['portal']
    #     self.assertTrue("E-Deposit: Producent" in portal.validRoles(), 'role added')

    # def test_producents_group_added(self):
    #     portal = self.layer['portal']
    #     acl_users = portal['acl_users']
    #     self.assertEqual(1, len(acl_users.searchGroups(name='E-Deposit: Producents')),""" E-Deposit: Producents group added """)

    # def test_PloneFormGen_installed(self):
    #     portal = self.layer['portal']
    #     portal_types = getToolByName(portal, 'portal_types')
    #     self.assertTrue("FormFolder" in portal_types)

    # @withPortal
    # def test_epublication_setup(self, portal, **kwargs):
    #     fti = getContentType(portal, 'edeposit.content.epublication')
    #     allowed_content_types = frozenset(fti.allowed_content_types)
    #     self.assertTrue(allowed_content_types == frozenset(['edeposit.content.printingfile', 'edeposit.content.originalfile', 'edeposit.content.previewfile', 'edeposit.content.author', 'Collection']))
    #     self.assertTrue(fti.add_permission == 'edeposit.AddEPublication')
    #     # fti.__dict__
    #     # pass
    #     # #epublication.allowed_content_types
    #     # #context.allowedContentTypes()

    # @withPortal
    # def test_edeposit_permissions(self, portal, **kwargs):
    #     permissions = [ii[0] for ii in getPermissions()]
    #     for perm in ('E-Deposit: Add Producent','E-Deposit: Add ePublication', 
    #                  'E-Deposit: Add ePeriodical', 'E-Deposit: Add Book'
    #                  ):
    #         self.assertTrue(perm in permissions, "'%s' exists?" % (perm,))
        
    # @withPortal
    # def test_edeposit_permissions_for_assigned_producent(self, portal, **kwargs):
    #     availablePermissions = [ r['name'] for r in 
    #                              portal.permissionsOfRole('E-Deposit: Assigned Producent') if r['selected'] ]
    #     self.assertTrue('E-Deposit: Add ePublication' in availablePermissions, 'E-Deposit: Add ePublication')
    #     self.assertTrue('E-Deposit: Add ePeriodical' in availablePermissions, 'E-Deposit: Add ePeriodical')
    #     self.assertTrue('E-Deposit: Add Book' in availablePermissions, 'E-Deposit: Add Book')
        
    # def test_view_permisison_for_producent(self):
    #     portal = self.layer['portal']
    #     self.assertTrue('View' in [r['name']
    #                                for r in portal.permissionsOfRole('Reviewer')
    #                                if r['selected']])
    #     self.assertTrue('View' in [r['name']
    #                                for r in portal.permissionsOfRole('Publisher')
    #                                if r['selected']])

