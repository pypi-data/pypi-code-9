"""
This file demonstrates writing tests using the Tastypie test module. These will pass
when you run "manage.py test".

Test case for Model: SystemSetting
"""

from django.test import TestCase
from tastypie.test import ResourceTestCase

class SystemSettingTest(ResourceTestCase):
    fixtures = ['sample']

    def setUp(self):
        super(SystemSettingTest, self).setUp()
        self.url = "/thinrest/api/v1/"
        self.end_url = "/?format=json"
        self.GET = "GET"
        self.POST = "POST"
        self.DELETE = "DELETE"

    def get_url(self, resource_name, method_name, id=None):
        '''
        Method to build resource URL for specific operation
        '''
        if method_name == self.GET and not id:
            return self.url + resource_name + self.end_url
        elif method_name == self.GET and id:
            return self.url + resource_name + "/" + str(id) + self.end_url
        elif method_name == self.POST:
            return self.url + resource_name + "/"
        elif method_name == self.DELETE:
            return self.url + resource_name + "/" + str(id) + "/"

    def test_setting1_get_list(self):
        """
        Test case for getting setting list
        """
        print "Getting setting List.. ",
        resp = self.api_client.get(self.get_url("setting", self.GET), format='json')
        self.assertHttpOK(resp)
        returned_data = self.deserialize(resp)
        self.assertTrue(len(returned_data["setting_list"]) >= 1)
        print "Success"

    def test_setting2_get_detail(self):
        """
        Test case for setting detail
        """
        print "Getting setting Detail.. ",
        resp = self.api_client.get(self.get_url("setting", self.GET, id="email"), format='json')
        self.assertHttpOK(resp)
        returned_data = self.deserialize(resp)
        self.assertEqual(returned_data['value'], '1')
        print "Success"

    def test_setting3_create(self):
        """
        Test case for creating new setting
        """
        print "Creating New setting.. ",
        self.post_data = {
                    "name": "sms",
                    "value": '0'
                }
        resp = self.api_client.post(self.get_url("setting", self.POST), format='json',data=self.post_data)
        self.assertHttpCreated(resp)
        returned_data = self.deserialize(resp)
        self.assertEqual(returned_data['name'], "sms")
        self.assertEqual(returned_data['value'], '0')
        print "Success"

    def test_setting4_edit(self):
        """
        Test case for creating new setting
        """
        print "Editing setting.. ",
        self.post_data = {
                    "name": "email",
                    "value": '0'
                }
        resp = self.api_client.post(self.get_url("setting", self.POST), format='json',data=self.post_data)
        self.assertHttpCreated(resp)
        returned_data = self.deserialize(resp)
        self.assertEqual(returned_data['value'], '0')
        print "Success"

    def test_setting5_delete(self):
        """
        Tests case for delete setting
        """
        print "Deleting setting.. ",
        resp = self.api_client.delete(self.get_url("setting", self.DELETE, id="email"), format='json')
        self.assertHttpAccepted(resp)
        print "Success"
