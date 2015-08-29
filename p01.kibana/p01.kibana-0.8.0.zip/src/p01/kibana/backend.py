###############################################################################
#
# Copyright (c) 2013 Projekt01 GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
###############################################################################
"""Elasticsearch upd backend
$Id: backend.py 4354 2015-08-29 16:07:38Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import sys
import logging
import traceback

import elasticsearch

# priority: ujson > simplejson > jsonlib2 > json
priority = ['ujson', 'simplejson', 'jsonlib2', 'json']
for mod in priority:
    try:
        json = __import__(mod)
    except ImportError:
        pass
    else:
        break


logger = logging.getLogger('p01.kibana.backend')


def getHosts(value):
    if ',' in value:
        hosts = value.split(',')
    elif isinstance(value, basestring) and value:
        hosts = [value]
    elif isinstance(value, (list, tuple)):
        hosts = list(hosts)
    else:
        hosts = ['0.0.0.0:9200']
    return hosts


class ElasticSearchBackend(object):
    """Sends event data to one or more elasticsearch server"""

    def __init__(self, server, hosts=['0.0.0.0:9200'], timeout=4):
        self.server = server
        self._hosts = getHosts(hosts)
        self.es = elasticsearch.Elasticsearch(self._hosts, timeout=timeout)

    def send(self, iterable):
        """Send messages to elasticsearch server

        We received the following data from our client. See KibanaClient and
        KibanaServer:

        {
            '_index': '...',
            '_type': '...',
            '_source': {
                '@version': '...',
                '@timestamp': '...',
                'message': '...'
            }
        }

        """
        for data in iterable:
            try:
                index = data['_index']
                doc_type = data['_type']
                body = data['_source']
                if hasattr(body, 'encode'):
                    body = body.encode('utf-8')
                self.es.index(index, doc_type, body)
            except Exception, ex:
                extra = {'data': "Data: %s" % json.dumps(data)}
                logger.exception(ex, extra=extra)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, ','.join(self._hosts))
