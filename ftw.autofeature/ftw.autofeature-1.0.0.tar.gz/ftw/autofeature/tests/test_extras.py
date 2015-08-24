from ftw.autofeature.tests import ZCMLTestCase


class TestExtrasFeaturesAreAutomaticallyRegistered(ZCMLTestCase):

    def test_zcml_feature_registered_when_using_utility(self):
        test_feature_name = 'ftw.autofeature:tests'
        self.assert_feature_not_provided(test_feature_name)

        self.load_zcml('<include package="ftw.autofeature" file="meta.zcml" />')
        self.assert_feature_not_provided(test_feature_name)

        self.load_zcml('<autofeature:extras />')
        self.assert_feature_provided(test_feature_name)

        self.assert_feature_provided('ftw.autofeature:tests')
        self.assert_feature_provided('ftw.autofeature:example')
        self.assert_feature_provided('ftw.autofeature:example:tests')
        self.assert_feature_provided('ftw.autofeature:tests:example')
