"""
This file demonstrates writing tests using the Tastypie test module. These will pass
when you run "manage.py test".

Test case for Model: Employee
"""

from django.test import TestCase
from tastypie.test import ResourceTestCase

class EmployeeTest(ResourceTestCase):
    fixtures = ['sample']

    def setUp(self):
        super(EmployeeTest, self).setUp()
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

    def test_employee1_get_list(self):
        """
        Test case for getting employee list
        """
        print "Getting Employee List.. ",
        resp = self.api_client.get(self.get_url("employee", self.GET), format='json')
        self.assertHttpOK(resp)
        returned_data = self.deserialize(resp)
        self.assertTrue(len(returned_data["employee_list"]) >= 1)
        print "Success"

    def test_employee2_get_detail(self):
        """
        Test case for employee detail
        """
        print "Getting Employee Detail.. ",
        resp = self.api_client.get(self.get_url("employee", self.GET, id=1), format='json')
        self.assertHttpOK(resp)
        returned_data = self.deserialize(resp)
        self.assertEqual(returned_data['first_name'], "Anurag")
        self.assertEqual(returned_data['last_name'], "Agarwal")
        self.assertEqual(returned_data['address'], "Wakad")
        self.assertEqual(returned_data['city'], "Pune")
        self.assertEqual(returned_data['state'], "Maharashtra")
        self.assertEqual(returned_data['zip_code'], '411057')
        print "Success"

    def test_employee3_create(self):
        """
        Test case for creating new employee
        """
        print "Creating New Employee.. ",
        self.post_data = {
                    "first_name": "Test",
                    "last_name": "User",
                    "address": "Abcd",
                    "city": "Pune",
                    "state": "Maharashtra",
                    "zip_code": "411057"
                }
        resp = self.api_client.post(self.get_url("employee", self.POST), format='json',data=self.post_data)
        self.assertHttpCreated(resp)
        returned_data = self.deserialize(resp)
        self.assertEqual(returned_data['first_name'], "Test")
        self.assertEqual(returned_data['last_name'], "User")
        self.assertEqual(returned_data['address'], "Abcd")
        self.assertEqual(returned_data['city'], "Pune")
        self.assertEqual(returned_data['state'], "Maharashtra")
        self.assertEqual(returned_data['zip_code'], '411057')
        print "Success"

    def test_employee4_edit(self):
        """
        Test case for creating new employee
        """
        print "Editing Employee.. ",
        self.post_data = {
                    "id": 1,
                    "zip_code": "411058"
                }
        resp = self.api_client.post(self.get_url("employee", self.POST), format='json',data=self.post_data)
        self.assertHttpCreated(resp)
        returned_data = self.deserialize(resp)
        self.assertEqual(returned_data['zip_code'], '411058')
        print "Success"

    def test_employee5_delete(self):
        """
        Tests case for delete employee
        """
        print "Deleting Employee.. ",
        resp = self.api_client.delete(self.get_url("employee", self.DELETE, id=1), format='json')
        self.assertHttpAccepted(resp)
        print "Success"
