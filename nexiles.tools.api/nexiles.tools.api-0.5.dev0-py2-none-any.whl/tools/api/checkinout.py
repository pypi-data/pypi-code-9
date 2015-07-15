# -*- coding: utf-8 -*-
#
# File: checkinout.py
#
# Copyright (c) nexiles GmbH
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'


import logging

from nexiles.tools.api import validators
from nexiles.tools.api import get_resource
from nexiles.tools.api import utils


logger = logging.getLogger("nexiles.tools.api")


__all__ = ["checkin", "checkout", "undo_checkout", "add_commands"]


@utils.decode_response
@utils.handle_http_errors
def checkout(resource, oid, message):
    """checkout(resource, oid, message) -> new business object iteration

    Check out business object and return new iteration.

    :param resource:    The resource -- see :py:func:`nexiles.tools.api.get_resource`
    :param oid:         The OID of the business object
    :param message:     The checkout message

    :returns: new business object iteration
    """
    info = {
        "message": message
    }
    logger.debug("checkout info: %r" % info)
    response = resource(oid).checkout().post(info)
    logger.debug("post return: %r" % response)
    return response


@utils.decode_response
@utils.handle_http_errors
def checkin(resource, oid, message):
    """checkin(resource, oid, message) -> new_doc

    Check in a checked out document.

    :param resource:    The resource -- see :py:func:`nexiles.tools.api.get_resource`
    :param oid:         The OID of the business object
    :param message:     The checkout message

    :returns: new business object iteration
    """
    info = {
        "message": message
    }
    logger.debug("checkout info: %r" % info)
    response = resource(oid).checkin().post(info)
    logger.debug("post return: %r" % response)
    return response


@utils.decode_response
@utils.handle_http_errors
def undo_checkout(resource, oid):
    """undo_checkout(resource, oid) -> doc

    Reverts a checkout.

    :param resource:    The resource -- see :py:func:`nexiles.tools.api.get_resource`
    :param oid:         The OID of the business object

    :returns: previous iteration
    """
    response = resource(oid).undo_checkout().post({})
    logger.debug("post return: %r" % response)
    return response

######################################################################
######################################################################
######################################################################


def command_ci(api, args):
    resource = get_resource(api, args.type)
    doc = utils.get_object(resource, args.oid)
    print "current iteration: ", utils.object_pretty_print(doc)

    if not utils.object_is_checked_out(resource, args.oid):
        raise RuntimeError("The business object at '%s' is not checked out." % args.oid)

    new_doc = checkin(resource, args.oid, args.message)

    new_doc = utils.get_object(resource, new_doc.oid)

    print "new     iteration: ", utils.object_pretty_print(new_doc)
    print
    print "check in complete."


def command_co(api, args):
    resource = get_resource(api, args.type)
    doc = utils.get_object(resource, args.oid)
    print "current iteration: ", utils.object_pretty_print(doc)

    if not utils.object_is_latest_iteration(resource, args.oid):
        raise RuntimeError("The business object at '%s' is not the latest iteration." % args.oid)

    new_doc = checkout(resource, args.oid, args.message)

    new_doc = utils.get_object(resource, new_doc.oid)

    print "new     iteration: ", utils.object_pretty_print(new_doc)
    print
    print "checkout complete."


def command_undo(api, args):
    resource = get_resource(api, args.type)

    doc = utils.get_object(resource, args.oid)
    print "current iteration: ", utils.object_pretty_print(doc)

    if not utils.object_is_checked_out(resource, args.oid):
        raise RuntimeError("The business object at '%s' is not checked out." % args.oid)

    new_doc = undo_checkout(resource, args.oid)

    new_doc = utils.get_object(resource, new_doc.oid)

    print "new     iteration: ", utils.object_pretty_print(new_doc)
    print
    print "checkout reverted."


def add_commands(subparsers, defaults):
    subparser = subparsers.add_parser("checkin")
    subparser.add_argument("--oid", required=True, dest="oid", type=validators.is_oid)
    subparser.add_argument("--message", required=True, dest="message", type=str)
    subparser.add_argument("--type",
            dest="type",
            default=defaults.default_type,
            type=validators.is_resource("part", "document", "epmdocument"))
    subparser.set_defaults(command=command_ci)

    subparser = subparsers.add_parser("checkout")
    subparser.add_argument("--oid", required=True, dest="oid", type=validators.is_oid)
    subparser.add_argument("--message", required=True, dest="message", type=str)
    subparser.add_argument("--type",
            dest="type",
            default=defaults.default_type,
            type=validators.is_resource("part", "document", "epmdocument"))
    subparser.set_defaults(command=command_co)

    subparser = subparsers.add_parser("undo-checkout")
    subparser.add_argument("--oid", required=True, dest="oid", type=validators.is_oid)
    subparser.add_argument("--type",
            dest="type",
            default=defaults.default_type,
            type=validators.is_resource("part", "document", "epmdocument"))
    subparser.set_defaults(command=command_undo)


# vim: set ft=python ts=4 sw=4 expandtab :
