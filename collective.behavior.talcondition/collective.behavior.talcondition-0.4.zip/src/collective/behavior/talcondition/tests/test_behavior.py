# -*- coding: utf-8 -*-
from plone.app.testing import login
from plone.app.testing import TEST_USER_NAME
from collective.behavior.talcondition.testing import IntegrationTestCase
from collective.behavior.talcondition.behavior import ITALCondition


class TestBehavior(IntegrationTestCase):

    def setUp(self):
        """ """
        super(TestBehavior, self).setUp()
        # create a testitem
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory(id='testitem',
                                  type_name='testtype',
                                  title='Test type')
        self.testitem = self.portal.testitem
        self.adapted = ITALCondition(self.testitem)

    def test_behavior(self):
        """Test that once enabled, the behavior do the job."""
        self.assertFalse(hasattr(self.testitem, 'tal_condition'))
        # adapted is ITALCondition(self.testitem)
        # it has a 'tal_condition' attribute
        self.assertTrue(hasattr(self.adapted, 'tal_condition'))
        # set a tal_condition and evaluate
        # this is True
        self.adapted.tal_condition = u"python:context.portal_type=='testtype'"
        self.assertTrue(self.adapted.evaluate())
        # this is False
        self.adapted.tal_condition = u"python:context.portal_type=='unexisting_portal_type'"
        self.assertFalse(self.adapted.evaluate())

    def test_wrong_condition(self):
        """In case the condition is wrong, it just returns False
           and a message is added to the Zope log."""
        # using a wrong expression does not break anything
        self.adapted.tal_condition = u'python: context.some_unexisting_method()'
        self.assertFalse(self.adapted.evaluate())

    def test_evaluate_extra_expr_ctx(self):
        """The 'evaluate' method can receive a 'extra_expr_ctx' dict
           that will extend the TAL expression context."""
        self.adapted.tal_condition = "python: value == '122'"
        self.assertFalse(self.adapted.evaluate())
        self.assertTrue(self.adapted.evaluate(extra_expr_ctx={'value': '122'}))
