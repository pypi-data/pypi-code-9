#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import requests, json, datetime, zlib

from . import util, issues

class Service:
    """
    :param host:
    :param user:
    :param password:
    :param version:
    :param pretty:
    """
    def __init__(self, host, user, password, version, pretty):
        if not host.startswith('http'):
            host = 'http://%s' % host

        self.host = host

        self.version = version
        self.pretty = pretty

        self.session = requests.Session()
        self.session.headers.update({
            'content-type': 'application/json',
            'accept': 'application/json; charset=utf8'
            })

        if user is not None and password is not None:
            self.session.auth = (user, password)

    def _format_(self, arg, pretty):
        """_format_

        :param arg:
        :param pretty:
        """
        if pretty:
            return util.pretty(arg)
        else:
            return arg

    def request(self, method, path, accept = 200, data = None, files = None, headers = {}):
        """request

        :param method:
        :param path:
        :param accept:
        :param data:
        :param files:
        :param headers:
        """
        URI = '{host}/{version}/{path}'.format(host=self.host, version=self.version, path=path)
        result = method(URI, data=json.dumps(data), files=files, headers = headers)

        # TODO: if gzip compression is enabled in jira it is necessary to decompress in case users enter false login information.
        #
        # if 'content-encoding' in result.headers and result.headers['content-encoding'] == 'gzip':
        #     content = zlib.decompress(result.content, 16+zlib.MAX_WBITS)
        # else:
        #     content = result.text

        if result.status_code != accept:
            message = 'failed to run %s on %s with returncode %s and message: "%s"' % (
                    method.__name__, URI, result.status_code,
                    result.text)
            if data is not None:
                message += '\ndata was: "%s"' % data
            if files is not None:
                message += '\nfiles was: %s' % files
            raise Exception(message)

        try:
            return result.json()
        except:
            logging.debug('json parsing failed, returning text: %s', e)
            return result.text

    def get(self, path, pretty, accept = 200, headers = {}):
        return self._format_(
                self.request(
                    self.session.get, path, accept=accept, headers=headers),
                    pretty)

    def post(self, path, pretty, accept = 200, data = None, files = None, headers = {}):
        return self._format_(
                self.request(
                    self.session.post, path, accept=accept, data=data, files=files, headers=headers),
                    pretty)

    def put(self, path, pretty, accept = 200, data = None, files = None, headers = {}):
        return self._format_(
                self.request(
                    self.session.put, path, accept=accept, data=data, files=files, headers=headers),
                    pretty)

    def delete(self, path, pretty, accept = 200, data = None, files = None, headers = {}):
        return self._format_(
                self.request(
                    self.session.delete, path, accept=accept, data=data, files=files, headers=headers),
                    pretty)

    def myself(self):
        """myself"""
        return self.get('myself', self.pretty)

    def projects(self, max_results):
        """projects

        :param max_results:
        """
        return self.get('project&maxResults={mr}'.format(mr = max_results), self.pretty)

    def issues(self, max_results, fields, filter_list):
        """issues

        :param max_results:
        :param fields:
        :param filter_list:
        """
        data = { "jql": util.create_jql(filter_list), "maxResults": max_results }

        if fields is not None and fields != []:
            data["fields"] = fields

        return self.post('search', self.pretty, data = data)

    def worklog(self, max_results, filter_list):
        """issues
        TODO: this method is pretty ugly

        :param max_results:
        :param fields:
        :param filter_list:
        """
        data = { "jql": util.create_jql(filter_list),
                 "maxResults": max_results,
                 "fields": ['customfield_10002', 'customfield_10004', 'assignee', 'summary', 'parent']
                 }

        result = self.post('search', False, data = data)

        summary = { 'total_hours': 0,
                    'estimate'   : 0,
                    'velocity'   : 0
                   }

        for entry in result['issues']:
            issue = issues.Issue.from_api(entry, filter_list)

            if issue is not None:
                for entry in self.get('issue/%s/worklog' % issue.key, False)['worklogs']:
                    issue.log_work(issues.Worklog.from_api(entry))
                summary.update(issue.to_dict())

                summary['total_hours'] += issue.total_hours
                summary['estimate'] += issue.estimate

        summary['velocity'] = util.calculate_velocity(summary['estimate'], summary['total_hours'])

        return self._format_(summary, self.pretty)

    def users(self, max_results):
        return self.get("user&maxResults={mr}".format(mr = max_results), self.pretty)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
