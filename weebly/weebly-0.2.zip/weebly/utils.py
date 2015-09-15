import requests
import hashlib
import hmac
import json
import base64


base_url = 'https://api.weeblycloud.com/'


class WeeblyClient(object):

    def __init__(self, api_key, api_secret):
        self.WEEBLY_API_KEY         = api_key
        self.WEEBLY_API_SECRET      = api_secret


    def weebly_hash(self, my_content):
        my_hmac = hmac.new(self.WEEBLY_API_SECRET, my_content, digestmod=hashlib.sha256).hexdigest()
        my_hash = base64.b64encode(my_hmac)

        return my_hash


    def post(self, my_url, my_data=None):

        # get url
        full_url = base_url + my_url

        # get hash
        if (my_data == None):
            my_content = 'POST' + '\n' + my_url + '\n'
        else:
            my_content = 'POST' + '\n' + my_url + '\n' + json.dumps(my_data)

        my_hash = self.weebly_hash(my_content)

        # get headers
        if (my_data == None):
            post_header = {
                'X-Public-Key': self.WEEBLY_API_KEY,
                'X-Signed-Request-Hash': my_hash,
            }
        else:
            post_header = {
                'Content-Type': 'application/json',
                'X-Public-Key': self.WEEBLY_API_KEY,
                'X-Signed-Request-Hash': my_hash,
            }

        # send request
        if (my_data == None):
            resp = requests.post(full_url, headers=post_header)
        else:
            resp = requests.post(full_url, data=json.dumps(my_data), headers=post_header)

        return resp


    def get(self, my_url):

        # get url
        full_url = base_url + my_url

        # get hash
        my_content = 'GET' + '\n' + my_url + '\n'
        my_hash = self.weebly_hash(my_content)

        # get headers
        get_header = {
            'X-Public-Key': self.WEEBLY_API_KEY,
            'X-Signed-Request-Hash': my_hash,
        }

        # send request
        resp = requests.get(full_url, headers=get_header)

        return resp


    def put(self, my_url, my_data):
        # get url
        full_url = base_url + my_url

        # get hash
        my_content = 'PUT' + '\n' + my_url + '\n' + json.dumps(my_data)
        my_hash = self.weebly_hash(my_content)

        # get headers
        put_header = {
            'Content-Type': 'application/json',
            'X-Public-Key': self.WEEBLY_API_KEY,
            'X-Signed-Request-Hash': my_hash,
        }

        # send request
        resp = requests.put(full_url, data=json.dumps(my_data), headers=put_header)

        return resp


    def patch(self, my_url, my_data):
        # get url
        full_url = base_url + my_url

        # get hash
        my_content = 'PATCH' + '\n' + my_url + '\n' + json.dumps(my_data)
        my_hash = self.weebly_hash(my_content)

        # get headers
        patch_header = {
            'Content-Type': 'application/json',
            'X-Public-Key': self.WEEBLY_API_KEY,
            'X-Signed-Request-Hash': my_hash,
        }

        # send request
        resp = requests.patch(full_url, data=json.dumps(my_data), headers=patch_header)

        return resp


    def delete(self, my_url):
        full_url = base_url + my_url

        #get hash
        my_content = 'DELETE' + '\n' + my_url + '\n'
        my_hash = self.weebly_hash(my_content)

        # get headers
        post_header = {
            'X-Public-Key': self.WEEBLY_API_KEY,
            'X-Signed-Request-Hash': my_hash,
        }

        # send request
        resp = requests.delete(full_url, headers=post_header)

        return resp


