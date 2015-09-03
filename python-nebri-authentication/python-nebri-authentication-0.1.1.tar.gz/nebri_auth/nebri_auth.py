from nebri_client import NebriClient
import base64


class NebriToken(NebriClient):
    def __init__(self, instance_name, token):
        self.token = token
        super(NebriToken, self).__init__(instance_name)

    def api_request(self, api_module, view_name, method='GET', headers={}, payload=None, files=None):
        if payload is None:
            payload = {'token': self.token}
        else:
            payload['token'] = self.token
        return super(NebriToken, self).api_request(api_module, view_name, method=method, headers=headers,
                                                     payload=payload, files=files)


class NebriBasic(NebriClient):
    def __init__(self, instance_name, username, password):
        self.username = username
        self.password = password
        super(NebriBasic, self).__init__(instance_name)

    def api_request(self, api_module, view_name, method='GET', headers={}, payload=None, files=None):
        return super(NebriBasic, self).api_request(api_module, view_name, method=method, headers=headers,
                                                     payload=payload, files=files, auth=(self.username, self.password))


class NebriOAuth(NebriClient):
    def __init__(self, instance_name, access_token=None, consumer_key=None, consumer_secret=None):
        self.access_token = access_token
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        super(NebriOAuth, self).__init__(instance_name)

    def api_request(self, api_module, view_name, method='GET', headers={}, payload=None, files=None):
        if self.access_token is None:
            if self.consumer_key is None or self.consumer_secret is None:
                raise Exception('Consumer Key and Consumer Secret is required.')
            else:
                params = {'key': self.consumer_key, 'secret': self.consumer_secret}
                response = super(NebriOAuth, self).api_request('nebrios_authentication', 'get_oauth_token',
                                                                 method="POST", payload=params)
                if response == "<class 'core.http.HttpResponseForbidden'>":
                    return 'Consumer Key or Consumer Secret are incorrect.'
                self.access_token = response['access_token']
        if payload is None:
            payload = {'access_token': self.access_token}
        else:
            payload['access_token'] = self.access_token
        return super(NebriOAuth, self).api_request(api_module, view_name, method=method, headers=headers,
                                                     payload=payload, files=files)

