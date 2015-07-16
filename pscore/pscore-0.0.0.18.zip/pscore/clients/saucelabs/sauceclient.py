import json

import requests
import sys


__version__ = '0.1.0'


class SauceClient(object):
    def __init__(self, sauce_username=None, sauce_access_key=None):
        self.sauce_username = sauce_username
        self.sauce_access_key = sauce_access_key
        self.headers = self.make_headers()
        self.information = Information(self)
        self.jobs = Jobs(self)
        self.provisioning = Provisioning(self)
        self.usage = Usage(self)

    def make_headers(self):
        python_version = sys.version_info[0]
        if python_version > 2:
            base64string = bytes('%s:%s' % (self.sauce_username, self.sauce_access_key), encoding='utf-8')[:-1]
        else:
            import base64
            base64string = base64.encodestring(
                '%s:%s' % (self.sauce_username, self.sauce_access_key)
            )[:-1]

        headers = {
            'Authorization': 'Basic %s' % base64string,
            'Content-Type': 'application/json',
        }
        return headers

    def request(self, method, url, body=None):
        if sys.version_info[0] < 3:
            result = self.request27(method=method, url=url, body=body)
            return result
        else:
            base_url = "https://{0}:{1}@saucelabs.com".format(self.sauce_username, self.sauce_access_key)
            full_url = base_url + url
            resp = requests.request(method, full_url, data=body, params=None)
            resp.raise_for_status()
            output = str(resp.json()).replace("'", '"').replace('None', '""').replace('True', '"True"').replace("False",
                                                                                                            '"False"')
            return output

    def request27(self, method, url, body=None):
        # this is a python 2.7 only module
        import httplib
        # Taken from https://raw.githubusercontent.com/cgoldberg/sauceclient/master/sauceclient.py
        connection = httplib.HTTPSConnection('saucelabs.com')
        connection.request(method, url, body, headers=self.headers)
        response = connection.getresponse()
        json_data = response.read()
        connection.close()
        if response.status != 200:
            raise Exception('%s: %s.\nSauce Status NOT OK' %
                            (response.status, response.reason))
        return json_data


class Jobs(object):
    def __init__(self, client):
        self.client = client

    def get_job_ids(self):
        """List all jobs id's belonging to the user."""
        method = 'GET'
        url = '/rest/v1/%s/jobs' % self.client.sauce_username
        json_data = self.client.request(method, url)
        jobs = json.loads(json_data)
        job_ids = [attr['id'] for attr in jobs]
        return job_ids

    def get_jobs(self):
        """List all jobs belonging to the user."""
        method = 'GET'
        url = '/rest/v1/%s/jobs?full=true' % self.client.sauce_username
        json_data = self.client.request(method, url)
        jobs = json.loads(json_data)
        return jobs

    def get_job_attributes(self, job_id):
        """Get information for the specified job."""
        method = 'GET'
        url = '/rest/v1/%s/jobs/%s' % (self.client.sauce_username, job_id)
        json_data = self.client.request(method, url)
        attributes = json.loads(json_data)
        return attributes

    def update_job(self, job_id, build_num=None, custom_data=None,
                   name=None, passed=None, public=None, tags=None):
        """Update attributes for the specified job."""
        content = {}
        if build_num is not None:
            content['build'] = build_num
        if custom_data is not None:
            content['custom-data'] = custom_data
        if name is not None:
            content['name'] = name
        if passed is not None:
            content['passed'] = passed
        if public is not None:
            content['public'] = public
        if tags is not None:
            content['tags'] = tags
        body = json.dumps(content)
        method = 'PUT'
        url = '/rest/v1/%s/jobs/%s' % (self.client.sauce_username, job_id)
        json_data = self.client.request(method, url, body=body)
        attributes = json.loads(json_data)
        return attributes


class Provisioning(object):
    def __init__(self, client):
        self.client = client

    def get_account_details(self):
        """Access account details."""
        method = 'GET'
        url = '/rest/v1/users/%s' % self.client.sauce_username
        json_data = self.client.request(method, url)
        attributes = json.loads(json_data)
        return attributes

    def get_account_limits(self):
        """Access account limits."""
        method = 'GET'
        url = '/rest/v1/%s/limits' % self.client.sauce_username
        json_data = self.client.request(method, url)
        attributes = json.loads(json_data)
        return attributes


class Information(object):
    def __init__(self, client):
        self.client = client

    def get_status(self):
        """Access the current status of Sauce Labs' services."""
        method = 'GET'
        url = '/rest/v1/info/status'
        json_data = self.client.request(method, url)
        status = json.loads(json_data)
        return status

    def get_browsers(self):
        """Get details of all browsers currently supported on Sauce Labs."""
        method = 'GET'
        url = '/rest/v1/info/browsers'
        json_data = self.client.request(method, url)
        browsers = json.loads(json_data)
        return browsers

    def get_count(self):
        """Get number of test executed so far on Sauce Labs."""
        method = 'GET'
        url = '/rest/v1/info/counter'
        json_data = self.client.request(method, url)
        count = json.loads(json_data)
        return count


class Usage(object):
    def __init__(self, client):
        self.client = client

    def get_current_activity(self):
        """Access current account activity.

        Returns active job counts broken down by job status and subaccount.
        """
        method = 'GET'
        url = '/rest/v1/%s/activity' % self.client.sauce_username
        json_data = self.client.request(method, url)
        activity = json.loads(json_data)
        return activity

    def get_historical_usage(self):
        """Access historical account usage."""
        method = 'GET'
        url = '/rest/v1/users/%s/usage' % self.client.sauce_username
        json_data = self.client.request(method, url)
        historical_usage = json.loads(json_data)
        return historical_usage