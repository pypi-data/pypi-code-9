# -*- coding: utf-8 -*-
from plone.app.testing import login
from plone.app.testing import TEST_USER_NAME
from collective.behavior.talcondition.testing import IntegrationTestCase
from collective.behavior.talcondition.behavior import ITALCondition


class TestBehavior(IntegrationTestCase):

    def test_behavior(self):
        """Test that once enabled, the behavior do the job."""
        # create a testitem
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory(id='testitem',
                                  type_name='testtype',
                                  title='Test type')
        testitem = self.portal.testitem
        self.assertFalse(hasattr(testitem, 'tal_condition'))
        # adapt the testitem
        adapted = ITALCondition(testitem)
        # now testitem has a 'tal_condition' attribute
        self.assertTrue(hasattr(adapted, 'tal_condition'))
        # set a tal_condition and evaluate
        # this is True
        adapted.tal_condition = u"python:context.portal_type=='testtype'"
        self.assertTrue(adapted.evaluate())
        # this is False
        adapted.tal_condition = u"python:context.portal_type=='unexisting_portal_type'"
        self.assertFalse(adapted.evaluate())

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
