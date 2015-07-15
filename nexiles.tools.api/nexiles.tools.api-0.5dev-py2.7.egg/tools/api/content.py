# -*- coding: utf-8 -*-
#
# File: content.py
#
# Copyright (c) nexiles GmbH
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'


import os
import base64
import logging

from nexiles.tools.api import validators
from nexiles.tools.api import get_resource
from nexiles.tools.api import utils


logger = logging.getLogger("nexiles.tools.api")


__all__ = ["create_content_info", "upload_content", "delete_content", "list_content", "command_list"]


def create_content_info(role, file_path, mimetype=None):
    """create_content_info(role, file_path, mimetype) -> mapping

    Create a content info dict used by the back end to add content to a
    business object.

    :param role:        The **role** of the new content item.
    :param file_path:   The path of the file to be uploaded.
    :param mimetype:    (optional) a mime type

    :returns: new business object iteration
    """
    file_name = os.path.basename(file_path)

    with file(file_path, "rb") as f:
        data = base64.encodestring(f.read())

    info = {
            role: [{
                "filename": file_name,
                "data":     data,
            }]
    }

    if mimetype is not None:
        info[role][0]["mimetype"] = mimetype

    return info


@utils.decode_response
@utils.handle_http_errors
def upload_content(resource, oid, role, file_path, mimetype=None, iterate=True, message="nxtools content upload"):
    """upload_content(resource, oid, role, file_path) -> new business object iteration

    Upload content to a business object of given resource type.

    .. note::  This will cause a *new iteration* of the business object.

    The `role` is one of the roles Windchill content items may have, like:

    - PRIMARY
    - SECONDARY
    - etc

    If no mime type is specified, the server will guess one based on the
    supplied file name.

    :param resource:    The resource -- see :py:func:`nexiles.tools.api.get_resource`
    :param oid:         The OID of the business object
    :param role:        The **role** of the new content item.
    :param file_path:   The path of the file to be uploaded.
    :param mimetype:    (optional) a mime type
    :param iterate:     whether or not to create a new iteration
    :param message:     the checkin/checkout message to use

    :returns: new business object iteration
    """
    info = create_content_info(role, file_path, mimetype)

    logger.debug("content info: %r" % info)
    response = resource(oid).content().post(info,
            iterate=iterate and "yes" or "no", message=message)
    logger.debug("post return: %r" % response)
    return response


@utils.decode_response
@utils.handle_http_errors
def delete_content(resource, oid, role, file_name, iterate=True, message="nxtools content delete"):
    """delete_content(resource, oid, role, filename) -> new_doc

    Delete named content item.

    .. note::  This will cause a *new iteration* of the business object.

    The `role` is one of the roles Windchill content items may have, like:

    - PRIMARY
    - SECONDARY
    - etc

    If `iterate` is set to False, then no new iteration is made automatically.
    The document is assumed to be checked out already.  The caller is
    resposnible to check in the document afterwards.

    If `iterate` is set to Ture (the default), then the message supplied in
    `message` is used for the check out and check in.

    :param resource:    The resource -- see :py:func:`nexiles.tools.api.get_resource`
    :param oid:         The OID of the business object
    :param role:        The **role** of the content item.
    :param filename:    The **name** of the content item to delete.
    :param iterate:     whether or not to create a new iteration
    :param message:     the checkin/checkout message to use

    :returns: new business object iteration
    """
    ret = resource(oid).content().delete(role=role, filename=file_name,
            iterate=iterate and "yes" or "no", message=message)
    logger.debug("delete return: %r" % ret)
    return ret


@utils.decode_response
@utils.handle_http_errors
def list_content(resource, oid, role=None):
    """list_content(resource, oid, role) -> sequence

    List the content items of the given business object.

    If `role` is given, filter by that role.

    The `role` is one of the roles Windchill content items may have, like:

    - PRIMARY
    - SECONDARY
    - etc

    :param resource:    The resource -- see :py:func:`nexiles.tools.api.get_resource`
    :param oid:         The OID of the business object
    :param role:        (optional) The **role** of the content item.

    :returns: sequence of content item infos
    """
    info = resource(oid).content().get()
    if role is not None:
        return filter(lambda i: i["role"] == role, info["items"])
    else:
        return info["items"]

######################################################################
######################################################################
######################################################################


def command_list(api, args):
    resource = get_resource(api, args.type)

    results = list_content(resource, args.oid, role=args.role)

    print "%d results" % len(results)
    for nr, item in enumerate(results):
        if nr == 0:
            print "%-4s %-15s %-35s %-20s" % ("nr", "role", "filename", "URL")
            print "-" * 75
        print "%03d:" % nr,  "%(role)-15s %(filename)-35s %(url)s" % item


def command_add(api, args):
    resource = get_resource(api, args.type)

    doc = utils.get_object(resource, args.oid)
    print "current iteration: ", utils.object_pretty_print(doc)

    if not utils.object_is_latest_iteration(resource, args.oid):
        raise RuntimeError("The business object at '%s' is not the latest iteration." % args.oid)

    if not args.iterate and not utils.object_is_checked_out(resource, args.oid):
        raise RuntimeError("The business object at '%s' is not checked out." % args.oid)

    new_doc = upload_content(resource, args.oid, args.role, args.filename,
            mimetype=args.mimetype, iterate=args.iterate, message=args.message)

    if args.iterate:
        new_doc = utils.get_object(resource, new_doc.oid)

        print "new     iteration: ", utils.object_pretty_print(new_doc)
        print

    print "content item upload complete."


def command_delete(api, args):
    resource = get_resource(api, args.type)

    doc = utils.get_object(resource, args.oid)
    print "current iteration: ", utils.object_pretty_print(doc)

    if not utils.object_is_latest_iteration(resource, args.oid):
        raise RuntimeError("The business object at '%s' is not the latest iteration." % args.oid)

    if not args.iterate and not utils.object_is_checked_out(resource, args.oid):
        raise RuntimeError("The business object at '%s' is not checked out." % args.oid)

    new_doc = delete_content(resource, args.oid, args.role, args.filename,
            iterate=args.iterate, message=args.message)

    if args.iterate:
        new_doc = utils.get_object(resource, new_doc.oid)

        print "new     iteration: ", utils.object_pretty_print(new_doc)
        print
    print "content item deleted."


def add_commands(subparsers, defaults):
    def add_args(parser, modify=False):
        parser.add_argument("--oid", required=True,
                dest="oid", type=validators.is_oid, help="the OID of the business object")
        parser.add_argument("--type",
                dest="type",
                default=defaults.default_type,
                type=validators.is_resource("part", "document", "epmdocument"),
                help="the resource type")
        parser.add_argument("--role", dest="role", type=str, help="the content role {PRIMARY|SECONDARY|THUMBNAIL|...}")
        if modify:
            parser.add_argument("--message", dest="message", type=str, help="commit message")
            parser.add_argument("--iterate", dest="iterate", default=True, action="store_true", help="automatically iterate")
            parser.add_argument("--no-iterate", dest="iterate", action="store_false", help="do NOT iterate")
        return parser

    subparser = subparsers.add_parser("content-list")
    subparser = add_args(subparser)
    subparser.set_defaults(command=command_list)

    subparser = subparsers.add_parser("content-add")
    subparser = add_args(subparser, True)
    subparser.add_argument("--mimetype", dest="mimetype", type=str, help="the mime type to use")
    subparser.add_argument("--filename", required=True, dest="filename", type=validators.is_file_path,
            help="local file to upload")
    subparser.set_defaults(command=command_add)

    subparser = subparsers.add_parser("content-delete")
    subparser = add_args(subparser, True)
    subparser.add_argument("--filename", required=True, dest="filename", type=str, help="name of the content item to delete")
    subparser.set_defaults(command=command_delete)


# vim: set ft=python ts=4 sw=4 expandtab :
