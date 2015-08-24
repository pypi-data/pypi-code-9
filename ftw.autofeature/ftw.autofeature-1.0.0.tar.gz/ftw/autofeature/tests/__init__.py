from unittest2 import TestCase
from zope.configuration import xmlconfig
from zope.configuration.config import ConfigurationMachine
from zope.configuration.xmlconfig import registerCommonDirectives


ZCML = '''
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:zcml="http://namespaces.zope.org/zcml"
    xmlns:autofeature="http://namespaces.zope.org/autofeature"
    package="ftw.autofeature.tests">
{}
</configure>
'''


class ZCMLTestCase(TestCase):

    def setUp(self):
        self.configuration_context = ConfigurationMachine()
        registerCommonDirectives(self.configuration_context)

    def tearDown(self):
        del self.configuration_context

    def load_zcml(self, *lines):
        zcml = ZCML.format('\n'.join(lines))
        xmlconfig.string(zcml, context=self.configuration_context)

    def assert_feature_provided(self, feature_name):
        self.assertTrue(
            self.configuration_context.hasFeature(feature_name),
            'The feature {} should now be registered.'.format(feature_name))

    def assert_feature_not_provided(self, feature_name):
        self.assertFalse(
            self.configuration_context.hasFeature(feature_name),
            'The feature {} should NOT be registered.'.format(feature_name))
