# -*- coding: utf-8 -*-
#
# File: utils.py
#
# Copyright (c) nexiles GmbH
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'


import re
import sys
import json
import time
import logging

from nexiles.tools.api import slumber

from functools import wraps

from nexiles.tools.api import tree

logger = logging.getLogger("nexiles.tools.api")

class NXToolsException(RuntimeError):
    pass

class NXToolsHTTPError(NXToolsException):

    def __init__(self, message, code, response):
        self.message = message
        self.code = code
        self.response = response

    def __repr__(self):
        return "<NXToolsHTTPError code %d: %s>" % (self.code, self.message)

def die(code, msg):
    logger.error(msg)
    print >>sys.stderr, msg
    sys.exit(code)

def handle_http_errors(func):
    @wraps(func)
    def wrapper(*args, **kw):
        try:
            value = func(*args, **kw)
        except (slumber.exceptions.HttpServerError, slumber.exceptions.HttpClientError), e:
            logger.error("HTTP ERROR: %r" % e)
            logger.error("code: %d" % e.response.status_code)
            logger.error("response: %s" % e.content)
            print_error(e.response.status_code, e.content)
            raise NXToolsHTTPError("HTTP ERROR: %r" %e, e.response.status_code, e.response)
        return value
    return wrapper


def decode(data):
    if isinstance(data, basestring):
        try:
            d = json.loads(data)
            decoded = tree.Tree(d)
            return decoded
        except ValueError:
            pass
    if type(data) == dict:
        return tree.Tree(data)
    return data


def decode_response(func):
    @wraps(func)
    def wrapper(*args, **kw):
        value = decode(func(*args, **kw))
        return value
    return wrapper


OR_REGEX = re.compile("(OR|VR):(.*):(\d+)")


def resource_from_oid(oid):
    m = OR_REGEX.match(oid)
    if m is None:
        raise ValueError("malformed OID")

    if len(m.groups()) != 3:
        raise ValueError("malformed OID")

    _, type_name, _ = m.groups()

    return {
        "wt.inf.container.OrgContainer": "organizations",
        "wt.pdmlink.PDMLinkProduct": "products",
        "wt.inf.library.WTLibrary": "libraries",
        "wt.projmgmt.admin.Project2": "projects",
        "wt.folder.SubFolder": "folders",
        "wt.folder.Cabinet": "cabinets",
        "wt.epm.EPMDocument": "epmdocuments",
        "wt.doc.WTDocument": "documents",
        "wt.part.WTPart": "parts",
        "wt.inf.team.ContainerTeam": "teams",
        "wt.org.WTGroup": "groups",
        "wt.org.WTUser": "users",
        "com.ptc.core.meta.type.mgmt.server.impl.WTTypeDefinition": "types",
        "wt.query.template.ReportTemplate": "reports",
        "com.ptc.windchill.wp.WorkPackage": "workpackages",
        "wt.epm.workspaces.EPMWorkspace": "workspaces",
    }[type_name]


@decode_response
@handle_http_errors
def get_object(resource, oid):
    doc = resource(oid).get()
    t = tree.Tree(doc)
    return t


@decode_response
@handle_http_errors
def query(resource, **kw):
    results = resource.get(**kw)
    return results["items"]


def object_exists(resource, oid):
    get_object(resource, oid)
    return True


def object_is_latest_iteration(resource, oid):
    doc = get_object(resource, oid)
    return doc.item.isLatestIteration is True


def object_is_checked_out(resource, oid):
    doc = get_object(resource, oid)
    return doc.item.isCheckedOut is True


def object_pretty_print(doc):
    return "%(name)-35s %(version)s %(state)s (%(number)-35s) %(oid)s" % doc.item


def prettyprint(func):
    @wraps(func)
    def wrapper(*args, **kw):
        value = func(*args, **kw)
        print json.dumps(value, indent=4)
        return value
    return wrapper


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kw):
        start = time.time()
        value = func(*args, **kw)
        duration = time.time() - start
        print "runtime: %3.3f seconds" % duration
        return value
    return wrapper


def print_error(code, content):
    print >>sys.stderr, "*" * 70
    print >>sys.stderr, "Server Error:"
    print >>sys.stderr, "code: ", code
    print >>sys.stderr, "response:"
    print >>sys.stderr, content
    print >>sys.stderr, "*" * 70

# vim: set ft=python ts=4 sw=4 expandtab :
