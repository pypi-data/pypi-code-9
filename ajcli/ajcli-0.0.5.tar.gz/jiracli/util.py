#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import re, json

def parse_duration_string(string):
    """TODO: Docstring for parse_duration_string.

    :string: TODO
    :returns: TODO

    """
    seconds = 0

    for token in re.findall(r'[0-9]+[a-z]', string.lower()):
        duration = token[:-1]
        if 'd' in token:
            seconds += int(duration) * 24 * 60 * 60
        elif 'h' in token:
            seconds += int(duration) * 60 * 60
        elif 'm' in token:
            seconds += int(duration) * 60
        elif 's' in token:
            seconds += int(duration)

    # TODO
    return round((seconds / 60.0) / 60.0, 2)

def create_jql(filter_list):
    """_create_jql_

    :param filter_list:
    """
    jql = ''
    for filter in filter_list:
        if jql != '':
            jql += ' AND %s' % filter
        else:
            jql += filter
    return jql

def pretty(arg):
    """_pretty_

    :param arg:
    """
    try:
        arg = [ json.loads(a.to_json()) for a in arg ]
    except:
        pass

    if isinstance(arg, str):
        arg = json.loads(arg)

    return json.dumps(arg, indent=4, sort_keys=True)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
