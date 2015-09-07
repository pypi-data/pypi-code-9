# -*- coding: utf-8 -*-

import json
import requests
import urllib


QIITA_URL = 'https://qiita.com/api/v2'
ERROR_CODES = [400, 401, 403, 404, 500]


def myself_items_url(page, per_page):
    """
        post item list take url

        Args
            page: int
            per_page: int

        Returns:
            url: str
    """
    return QIITA_URL + '/authenticated_user/items?page={}&per_page={}'.format(page, per_page)


def comments_url(comment_id):
    """
        post item related comment take url

        Args
            comment_id: int

        Returns:
          url: str
    """
    return QIITA_URL + '/items/{}/comments'.format(comment_id)


def tags_items_url(tag_id, page, per_page):
    return QIITA_URL + '/tags/{}/items?page={}&per_page={}'.format(tag_id, page, per_page)


def post_item_url():
    return QIITA_URL + '/items'


def stocks_url(user_id):
    return QIITA_URL + '/users/{}/stocks'.format(user_id)


def authenticated_user_url():
    return QIITA_URL + '/authenticated_user'


def stocks_url(user_id, page, per_page):
    return QIITA_URL + '/users/{}/stocks?page={}&per_page={}'.format(user_id, page, per_page)


class Qiita(object):

    def __init__(self, access_token):
        self._access_token = access_token

    def access_token(self):
        return 'Bearer {}'.format(self._access_token)

    def _urlencode(self, query):
        """
            Args:
                query: str
        """
        return urllib.parse.urlencode({'query': query})

    def authorization_header(self):
        return {
          'Authorization': self.access_token()
        }

    def json_request_header(self):
        header = self.authorization_header()
        header['Content-Type'] = 'application/json'
        return header

    def get_request(self, url, header):
        response = requests.get(url, headers=header)
        self._check_error(response)
        parsed_json = json.loads(response.text)
        return [item for item in parsed_json]

    def get_items(self, page=1, per_page=1):
        """
            Args:
                page: int
                per_page: int
            Returns:
                items: list[dict]
        """
        return self.get_request(myself_items_url(page, per_page), self.authorization_header())

    def get_comment(self, comment_id):
        """
            Args:
                comment_id: str
            Returns:
                comments: list[dict]
        """
        return self.get_request(comments_url(comment_id), self.authorization_header())

    def get_comments(self, comment_ids):
        """
            Args:
                comment_id: list[str]
            Returns:
                comments: list[dict]
        """
        comments = []
        for comment_id in comment_ids:
            comments.extend(self.get_comment(comment_id))

        return comments

    def get_tags_items(self, tag_id, page=1, per_page=1):
        return self.get_request(tags_items_url(tag_id, page, per_page), self.json_request_header())

    def get_stocks(self, user_id):
        return self.get_request(stocks_url(user_id), self.authorization_header())

    def get_authenticated_user(self):
        return self.get_request(authenticated_user_url(), self.authorization_header())

    def get_stocks(self, user_id, page=1, per_page=1):
        return self.get_request(stocks_url(user_id, page, per_page), self.authorization_header())

    def post_item(self, data):
        response = requests.post(post_item_url(), headers=self.json_request_header(), data=data)
        self._check_error(response)

    def _check_error(self, response):
        if response.status_code in ERROR_CODES:
            raise Exception(response.text)

