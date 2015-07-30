from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.models.session.Credentials import Credentials
from okta.models.session.Session import Session


class SessionsClient(ApiClient):
    def __init__(self, base_url, api_token):
        ApiClient.__init__(self, base_url + '/api/v1/sessions', api_token)

    # CRUD

    def create_session(self, username, password, additional_fields=None):
        creds = Credentials()
        creds.username = username
        creds.password = password
        params = {'additionalFields': additional_fields}
        response = ApiClient.post_path(self, '/', creds, params=params)
        return Utils.deserialize(response.text, Session)

    def create_session_with_cookie_token(self, username, password):
        return self.create_session(username, password, 'cookieToken')

    def create_session_with_cookie_token_url(self, username, password):
        return self.create_session(username, password, 'cookieTokenUrl')

    def create_session_with_session_token(self, session_token, additional_fields=None):
        data = {'sessionToken': session_token}
        params = {'additionalFields': additional_fields}
        response = ApiClient.post_path(self, '/', data, params=params)
        return Utils.deserialize(response.text, Session)

    def validate_session(self, id):
        response = ApiClient.get_path(self, '/' + str(id))
        return Utils.deserialize(response.text, Session)

    def extend_session(self, id):
        response = ApiClient.put_path(self, '/' + str(id), None)
        return Utils.deserialize(response.text, Session)

    def clear_session(self, id):
        ApiClient.delete_path(self, '/' + str(id))