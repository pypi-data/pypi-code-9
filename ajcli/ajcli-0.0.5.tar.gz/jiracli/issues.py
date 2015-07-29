#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import json

from . import util

class Issue():
    def __init__(self, key, description, assignee, estimate, worklog = []):
        """TODO: Docstring for __init__.

        :id: TODO
        :description: TODO
        :returns: TODO

        """
        self.key = key
        self.description = description
        self.assignee = assignee
        self.estimate = estimate

        self.worklog = {}
        self.total_hours = 0
        self.velocity = 0

        for log in worklog:
            self.log_work(log)

    def log_work(self, worklog):
        """TODO: Docstring for log_work.

        :worklog: TODO
        :returns: TODO

        """
        assert isinstance(worklog, Worklog)

        if worklog.author not in self.worklog:
            self.worklog[worklog.author] = worklog
        else:
            self.worklog[worklog.author].update(worklog)

        self.total_hours += worklog.total_hours
        self.velocity = round(self.estimate / float(self.total_hours), 2)

    def to_dict(self):
        """TODO: Docstring for to_dict.
        :returns: TODO

        """
        return {self.key: {
            'worklog': [ log.to_dict() for author,log in self.worklog.items() ],
            'assignee': self.assignee,
            'description': self.description,
            'estimate': self.estimate,
            'total_hours': self.total_hours,
            'velocity': self.velocity }
            }

    @classmethod
    def from_api(cls, issue):
        fields = issue['fields']

        key = issue['key']
        description = fields['summary']

        assignee = None
        total_hours = 0
        estimate = 0
        velocity = 0

        if 'customfield_10002' in fields and fields['customfield_10002'] is not None:
            estimate = int(fields['customfield_10002'])

        if 'assignee' in fields and fields['assignee'] is not None:
            assignee = fields['assignee']['displayName']

        return cls(key, description, assignee, estimate)

class Worklog(object):

    """Docstring for Worklog. """

    def __init__(self, author, total_hours, comment):
        """TODO: to be defined1. """
        self.author = author
        self.comments = [comment] if comment is not None and comment != "" else []
        self.total_hours = total_hours

    def update(self, other):
        self.total_hours += other.total_hours
        self.comments += other.comments

    def to_dict(self):
        """TODO: Docstring for to_dict.
        :returns: TODO

        """
        return { 'author': self.author,
                 'comments': self.comments,
                 'total_hours': self.total_hours
                 }

    @classmethod
    def from_api(cls, log):
        """TODO: Docstring for __json__.
        :returns: TODO

        """
        author_name = log['author']['displayName']
        time_spent = util.parse_duration_string(log['timeSpent'])
        comment = log['comment']

        return cls(author_name, time_spent, comment)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
