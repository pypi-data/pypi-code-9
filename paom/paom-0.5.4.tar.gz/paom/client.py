import json
import requests

from resources import *

BASE_URL = "https://paom.com"
API_URL = "%s%s" % (BASE_URL, "/api")
TOKEN_URL = "%s%s" % (BASE_URL, "/api-oauth2/token/")


class BaseRequest(object):

    def __init__(self, access_token):
        self.access_token = access_token

    def _convert_to_json(self, response):
        return json.loads(response.content)

    def _call_api(self, url, data={}, method="GET"):
        full_url = "%s%s" % (API_URL, url)
        headers = {
            'authorization': "Bearer {0}".format(self.access_token),
        }
        if method == "GET":
            response = requests.get(full_url, headers=headers)
        elif method == "POST" and data:
            response = requests.post(full_url, data=data, headers=headers)
        elif method == "PATCH" and data:
            response = requests.patch(full_url, data=data, headers=headers)
        elif method == "DELETE" and data:
            response = requests.delete(full_url, data=data, headers=headers)
        return self._convert_to_json(response)


class PaomAPIAuth(object):

    def __init__(self, username, password, client_id, client_secret):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret

    def _convert_to_json(self, response):
        return json.loads(response.content)

    def get_access_token(self):
        headers = {
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8"
        }
        data = {
            "username": self.username,
            "password": self.password,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "password"
        }
        response = requests.post(TOKEN_URL, data=data, headers=headers)
        return self._convert_to_json(response)


class PaomAPI(object):

    def __init__(self, access_token):
        self.access_token = access_token
        self.request = self._initialize_base_request()

    def _initialize_base_request(self):
        return BaseRequest(self.access_token)

    @property
    def products(self):
        return Products(self.request)

    @property
    def users(self):
        return Users(self.request)

    @property
    def collections(self):
        return Collections(self.request)

    @property
    def categories(self):
        return Categories(self.request)

    @property
    def orders(self):
        return Orders(self.request)

    @property
    def carts(self):
        return Carts(self.request)

    @property
    def cart_items(self):
        return CartItems(self.request)

    @property
    def quizzes(self):
        return Quizzes(self.request)

    @property
    def questions(self):
        return Questions(self.request)

    @property
    def answers(self):
        return Answers(self.request)

    @property
    def user_answers(self):
        return UserAnswers(self.request)

    @property
    def user_results(self):
        return UserResults(self.request)

    @property
    def quiz_results(self):
        return QuizResults(self.request)
