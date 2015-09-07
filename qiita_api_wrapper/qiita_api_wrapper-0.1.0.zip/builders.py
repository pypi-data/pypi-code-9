# -*- coding: utf-8 -*-

import json


class PostBuilder(object):

    def __init__(self):
        self.parameters = {
            'title': '',
            'body': '',
            'coediting': False,
            'gist': False,
            'private': False,
            'tags': [],
            'tweet': False
        }

    def body(self, content):
        """
            Args:
                content: str
        """
        self.parameters['body'] = content
        return self

    def coediting(self, flag):
        """
            Args:
                flag: bool
        """
        self.parameters['coediting'] = flag
        return self

    def gist(self, flag):
        """
        Args:
            flag: bool
        """
        self.parameters['gist'] = flag
        return self

    def private(self, flag):
        """
            Args:
                flag: bool
        """
        self.parameters['private'] = flag
        return self

    def tags(self, t):
        """
            Args:
                t: list[dict]
                example : {"name": "tag_name", "versions": ["1.0"]}
        """
        self.parameters['tags'] = t
        return self

    def title(self, t):
        self.parameters['title'] = t
        return self

    def tweet(self, flag):
        self.parameters['tweet'] = flag
        return self

    def __str__(self):
        return json.dumps(self.parameters)

    def encode(self):
        """
            Returns:
                condoded request json string
        """
        return str(self).encode('utf-8')
