#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import json, re

from . import util

class Issue():
    def __init__(self, key, description, assignee, estimate, parent, worklog = []):
        """TODO: Docstring for __init__.

        :id: TODO
        :description: TODO
        :returns: TODO

        """
        self.key = key
        self.description = description
        self.assignee = assignee
        self.estimate = estimate
        self.parent = parent

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
        self.velocity = util.calculate_velocity(self.estimate, self.total_hours)

    def to_dict(self):
        """TODO: Docstring for to_dict.
        :returns: TODO

        """
        result = { self.key: {
            'worklog': [ log.to_dict() for author,log in self.worklog.items() ],
            'assignee': self.assignee,
            'description': self.description,
            'estimate': self.estimate,
            'total_hours': self.total_hours,
            'velocity': self.velocity }
            }

        if self.parent is not None:
            result[self.key]['parent'] = self.parent

        return result

    @classmethod
    def from_api(cls, issue, filter_list):
        fields = issue['fields']

        for entry in filter_list:
            if 'sprint=' in entry:
                sprint_id = int(entry.split('=')[1])
            for entry in fields['customfield_10004']:
                sprint = Sprint.from_api(entry)
                if sprint.key != sprint_id and sprint.state != 'CLOSED':
                    return

        key = issue['key']
        description = fields['summary']

        parent = None
        assignee = None
        total_hours = 0
        estimate = 0
        velocity = 0

        if 'customfield_10002' in fields and fields['customfield_10002'] is not None:
            estimate = int(fields['customfield_10002'])

        if 'assignee' in fields and fields['assignee'] is not None:
            assignee = fields['assignee']['displayName']

        if 'parent' in fields:
            parent = fields['parent']['key']

        return cls(key, description, assignee, estimate, parent)

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

class Sprint(object):

    """Docstring for Sprint. """

    def __init__(self, key, status, start_date, stop_date, complete_date):
        """TODO: to be defined1.

        :id: TODO
        :status: TODO
        :start_date: TODO
        :stop_date: TODO

        """
        self.key = key
        self.state = status
        self.start_date = start_date
        self.end_date = stop_date
        self.complete_date = complete_date

    def to_dict(self):
        """TODO: Docstring for to_dict.
        :returns: TODO

        """
        return { 'key': self.key,
                 'state': self.state,
                 'start_date': self.start_date,
                 'end_date': self.end_date,
                 'complete_date': self.complete_date
                 }

    @classmethod
    def from_api(cls, sprint):
        """TODO: Docstring for from_api.

        example:
            com.atlassian.greenhopper.service.sprint.Sprint@4ceff9a1[id=2,rapidViewId=1,state=CLOSED,name=Sprint 2,startDate=2015-07-03T13:00:53.070+02:00,endDate=2015-07-30T13:00:00.000+02:00,completeDate=2015-07-30T15:16:02.586+02:00,sequence=2]

        :sprint: TODO
        :returns: TODO

        """

        id = None
        state = None
        start_date = None
        end_date = None
        complete_date = None

        for foo in re.findall(r'[a-zA-Z]+=[a-zA-Z0-9-:+.]+', sprint):
            key, value = foo.split('=', 1)
            if key == 'id':
                id = int(value)
            elif key == 'state':
                state = value
            elif key == 'startDate':
                start_date = value
            elif key == 'endDate':
                end_date = value
            elif key == 'completeDate':
                complete_date = value

        return cls(id, state, start_date, end_date, complete_date)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
