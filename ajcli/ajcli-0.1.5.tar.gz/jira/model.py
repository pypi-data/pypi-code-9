#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import json, re, abc

from . import util

class Model(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def from_api(cls, *args, **kwargs):
        pass

    def to_dict(self):
        return { k: v for k,v in self.__dict__.items() if not k.startswith('_') }

class Issue(Model):
    def __init__(self, key, description, status, assignee, estimate, parent, link):
        """TODO: Docstring for __init__.

        :id: TODO
        :description: TODO
        :returns: TODO

        """
        self.key = key
        self.description = description
        self.status = status
        self.assignee = assignee
        self.parent = parent
        self.estimate = estimate
        self.link = link

        self.worklog = []
        self.total_hours = 0
        self.velocity = 0

    def log_work(self, worklog):
        if worklog.issue != self.key:
            raise Exception('incompatible worklog: %s' % worklog.to_dict())

        self.total_hours += worklog.total_hours
        self.velocity = util.calculate_velocity(self.estimate, self.total_hours)

        if self.worklog is None:
            self.worklog = []

        for log in self.worklog:
            if log.author == worklog.author:
                log += worklog
                return

        self.worklog.append(worklog)

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
        status = fields['status']['statusCategory']['key']
        link = issue['self']
        parent = None
        assignee = None
        estimate = 0

        if 'customfield_10002' in fields and fields['customfield_10002'] is not None:
            estimate = int(fields['customfield_10002'])

        if 'assignee' in fields and fields['assignee'] is not None:
            assignee = fields['assignee']['displayName']

        if 'parent' in fields:
            parent = fields['parent']['key']

        return cls(key, description, status, assignee, estimate, parent, link)

class Worklog(Model):

    """Docstring for Worklog. """

    def __init__(self, issue, author, total_hours, comment, link):
        """TODO: to be defined1. """
        self.issue = issue
        self.author = author
        self.total_hours = round(total_hours, 2)
        self.comments = [comment] if comment is not None and comment != "" else []
        self.links = [link] if link is not None and link != "" else []

    def update(self, other):
        self.total_hours += other.total_hours
        self.total_hours = round(self.total_hours, 2)
        self.comments += other.comments

    def __iadd__(self, other):
        if self.issue == other.issue and self.author == other.author:
            self.total_hours += other.total_hours
            self.total_hours = round(self.total_hours, 2)
            self.comments += other.comments
            self.links += other.links
        else:
            raise Exception('incompatible worklogs: %s and %s' % (self.to_dict(), other.to_dict()))

    @classmethod
    def from_api(cls, log, issue):
        """TODO: Docstring for __json__.
        :returns: TODO

        """
        author_name = log['author']['displayName']
        time_spent = util.parse_duration_string(log['timeSpent'])
        comment = log['comment']
        link = log['self']

        return cls(issue, author_name, time_spent, comment, link)

class Sprint(Model):

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

class Project(Model):

    """Docstring for Sprint. """

    def __init__(self, key, name, link):
        """TODO: to be defined1.

        :id: TODO
        :status: TODO
        :start_date: TODO
        :stop_date: TODO

        """
        self.key = key
        self.name = name
        self.link = link

    @classmethod
    def from_api(cls, project):
        key = project['key']
        name = project['name']
        link = project['self']

        return cls(key, name, link)

class User(Model):

    """Docstring for Sprint. """

    def __init__(self, name, key, groups, email, active, link):
        """TODO: to be defined1.

        :id: TODO
        :status: TODO
        :start_date: TODO
        :stop_date: TODO

        """
        self.name = name
        self.key = key
        self.groups = groups
        self.email = email
        self.active = active
        self.link = link

    @classmethod
    def from_api(cls, user):
        """TODO: Docstring for from_api.

        :sprint: TODO
        :returns: TODO

        """
        name = user['name']
        key  = user['key']
        groups = None #user['groups'] # TODO
        email = user['emailAddress']
        active = user['active']
        link = user['self']

        return cls(name, key, groups, email, active, link)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
