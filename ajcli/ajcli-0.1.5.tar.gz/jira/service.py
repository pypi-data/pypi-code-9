#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import requests, json, datetime, zlib, logging

from . import util, model

log = logging.getLogger('jira')

class StatuscodeException(Exception):
    def __init__(self, response):
        super(StatuscodeException, self).__init__(response)
        self.status_code = response.status_code
        try:
            self.message = response.json()
        except:
            self.message = response.text

class Service:
    """
    :param host:
    :param user:
    :param password:
    :param version:
    """
    def __init__(self, host, user, password, version):
        if not host.startswith('http'):
            host = 'http://%s' % host

        self.host = host

        self.version = version

        self.session = requests.Session()
        self.session.headers.update({
            'content-type': 'application/json',
            'accept': 'application/json; charset=utf8'
            })

        if user is not None and password is not None:
            self.session.auth = (user, password)

    def __request__(self, method, path, accept = 200, data = None, files = None, headers = {}):
        """request

        :param method:
        :param path:
        :param accept:
        :param data:
        :param files:
        :param headers:
        """
        URI = '{host}/{version}/{path}'.format(host=self.host, version=self.version, path=path)
        response = method(URI, data=json.dumps(data), files=files, headers = headers)

        # TODO: if gzip compression is enabled in jira it is necessary to decompress in case users enter false login information.
        #
        # if 'content-encoding' in result.headers and result.headers['content-encoding'] == 'gzip':
        #     content = zlib.decompress(result.content, 16+zlib.MAX_WBITS)
        # else:
        #     content = result.text
        #
        # however this seems to create further problems. Something is wrong here with gzip compression!

        if response.status_code != accept:
            # message = 'failed to run %s on %s with returncode %s' % (method.__name__, URI, response.status_code)

            try:
                log.debug(response.json())
            except:
                log.debug(response.text)

            if data is not None:
                log.debug('data was: "%s"', data)
            if files is not None:
                log.debug('files were: %s', files)

            raise StatuscodeException(response)

        try:
            return response.json()
        except:
            logging.debug('json parsing failed, returning text: %s', e)
            return response.text

    def get(self, path, accept = 200, headers = {}):
        """get

        :param path:
        :param accept:
        :param headers:
        """
        return self.__request__(self.session.get, path, accept=accept, headers=headers)

    def post(self, path, accept = 200, data = None, files = None, headers = {}):
        """post

        :param path:
        :param accept:
        :param data:
        :param files:
        :param headers:
        """
        return self.__request__(self.session.post, path, accept=accept, data=data, files=files, headers=headers)

    def put(self, path, accept = 200, data = None, files = None, headers = {}):
        """put

        :param path:
        :param accept:
        :param data:
        :param files:
        :param headers:
        """
        return self.__request__(self.session.put, path, accept=accept, data=data, files=files, headers=headers)

    def delete(self, path, accept = 200, data = None, files = None, headers = {}):
        """delete

        :param path:
        :param accept:
        :param data:
        :param files:
        :param headers:
        """
        return self.__request__(self.session.delete, path, accept=accept, data=data, files=files, headers=headers)

    def myself(self):
        """myself"""
        return model.User.from_api(self.get('myself'))

    def user(self, max_results, name, key):
        """TODO: Docstring for user.

        :name: TODO
        :returns: TODO

        """
        if name is not None and name != '':
            user = self.get('user?username=%s' % name)
        elif key is not None and key != '':
            user = self.get('user?key=%s' % key)

        return model.User.from_api(user)

    def users(self, max_results, project):
        """users

        :param max_results:
        :param project:
        """
        return [ model.User.from_api(user) for user in self.get("user/assignable/search?project=%s" % project) ]

    def projects(self):
        """projects

        :param max_results:
        """
        return [ model.Project.from_api(project) for project in self.get('project') ]

    def issue(self, key, fields):
        """issue

        :param key:
        :param fields:
        """
        return model.Issue.from_api(self.get('issue/%s' % key))

    def issues(self, max_results, filter_list, worklogs, fields = []):
        """issues

        :param max_results:
        :param fields:
        :param filter_list:
        """
        data = { "jql": util.create_jql(filter_list), "maxResults": max_results }

        if fields is not None and fields != []:
            data["fields"] = fields

        for result in self.post('search', data = data)['issues']:
            issue = model.Issue.from_api(result, filter_list)

            if issue is not None:
                if worklogs:
                    for log in self.worklogs(issue.key):
                        if log is not None:
                            issue.log_work(log)
                yield issue

    def worklogs(self, issue):
        """worklog

        :param issue:
        """

        for result in self.get('issue/%s/worklog' % issue)['worklogs']:
            worklog = model.Worklog.from_api(result, issue)

            if worklog is not None:
                yield worklog

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
