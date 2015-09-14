# -*- coding: utf-8 -*-
from zope.interface import alsoProvides
from plone.app.testing import login
from plone.app.testing import TEST_USER_NAME
from collective.behavior.talcondition.testing import IntegrationTestCase
from collective.behavior.talcondition.behavior import ITALCondition
from collective.behavior.talcondition.interfaces import ITALConditionable
from collective.behavior.talcondition.utils import applyExtender
from collective.behavior.talcondition.utils import evaluateExpressionFor


class TestUtils(IntegrationTestCase):

    def test_wrong_condition(self):
        """In case the condition is wrong, it just returns False
           and a message is added to the Zope log."""
        # create a testitem
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory(id='testitem',
                                  type_name='testtype',
                                  title='Test type')
        testitem = self.portal.testitem
        adapted = ITALCondition(testitem)
        # using a wrong expression does not break anything
        adapted.tal_condition = u'python: context.some_unexisting_method()'
        self.assertFalse(adapted.evaluate())

    def test_apply_extender(self):
        """Test that existing objects are correctly updated
           after enabling extender for their meta_type."""
        # the extender is not enabled for "Folder"
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory(id='testfolder',
                                  type_name='Folder',
                                  title='Test folder')
        testfolder = self.portal.testfolder
        self.assertFalse(hasattr(testfolder, 'tal_condition'))
        self.assertFalse(ITALConditionable.providedBy(testfolder))
        # enable the extender for testfolder
        alsoProvides(testfolder, ITALConditionable)
        # the schema is not updated until we do it
        self.assertFalse(hasattr(testfolder, 'tal_condition'))
        applyExtender(self.portal, meta_types=('ATFolder', ))
        # now the field is available
        self.assertTrue(hasattr(testfolder, 'tal_condition'))

    def test_empty_condition(self):
        # create a testitem
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory(id='testitem',
                                  type_name='testtype',
                                  title='Test type')
        testitem = self.portal.testitem
        adapted = ITALCondition(testitem)
        # using a wrong expression does not break anything
        adapted.tal_condition = None
        self.assertTrue(adapted.evaluate())

    def test_bypass_for_manager(self):
        """In this case, no matter the expression is False,
           it will return True if current user is 'Manager'."""
        # create a testitem
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory(id='testitem',
                                  type_name='testtype',
                                  title='Test type')
        testitem = self.portal.testitem
        adapted = ITALCondition(testitem)
        # using a wrong expression does not break anything
        adapted.tal_condition = "python:False"
        self.assertFalse(evaluateExpressionFor(adapted))
        adapted.roles_bypassing_talcondition = [u'Manager']
        # as current user is Manager, he can bypass the expression result
        self.assertTrue(evaluateExpressionFor(adapted))
