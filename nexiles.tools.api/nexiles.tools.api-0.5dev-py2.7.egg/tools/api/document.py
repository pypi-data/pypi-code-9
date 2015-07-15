
# -*- coding: utf-8 -*-
#
# File: document.py
#
# Copyright (c) nexiles GmbH
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'


import json
import logging

import collections

from nexiles.tools.api import validators
from nexiles.tools.api import get_resource
from nexiles.tools.api import utils
from nexiles.tools.api import content


logger = logging.getLogger("nexiles.tools.api")


class Manifest(object):
    """
    Document Manifest

    This object is used to read, parse and validate a manifest file used by the
    document create API.

    The manifest is a simple JSON file.

    Manifest Format::

        {
            "number":       "4711",
            "name":         "document_name",
            "container":    "TestProduct",
            "folder":       "/Defaults/foo",
            "description":  "A Test Document"
            "attributes": {
                "CUSTOMER":        "nexiles",
                "DESCRIPTION_GER": "foo bar baz"
            },
            "files": [
                {"role": "PRIMARY", "file_path": "local_file.txt"},
                {"role": "SECONDARY", "file_path": "foo.jpg"},
                {"role": "SECONDARY", "file_path": "woot.json", "mimetype": "application/json"},
            ]
        }
    """
    def __init__(self, **kw):
        self.number = self.name = None
        self.folder = None
        self.description = None
        self.files = []
        self.attributes = {}
        self._content_infos = collections.defaultdict(list)
        self.__dict__.update(kw)
        self.validate()

    @classmethod
    def from_file(klass, path):
        """from_file(klass, path) -> new manifest object

        Create a new manifest from the file specified.

        :param path: the path to a manifest JSON file
        :returns:    new manifest object
        """
        with file(path, "r") as manifest:
            keys = json.loads(manifest.read())
            return klass(**keys)

    def validate(self):
        """validate() -> None

        Validate manifest.  Raises `AssertionError` on
        validation errors.
        """
        assert self.name, "name not set"
        assert self.container, "container not set"

    def get_content_info(self):
        """get_content_info() -> mapping

        Processes the `files` attribute of the manifest and
        creates a content info structure from it.

        .. note:: processing is done only once, the result is cached

        :returns: content info mapping
        """
        if len(self._content_infos) == 0:
            for file_info in self.files:
                role = file_info["role"]
                path = file_info["file_path"]
                content_info = content.create_content_info(role,
                        path, file_info.get("mimetype"))

                self._content_infos[role].append(content_info[role][0])
        return self._content_infos

    @property
    def content(self):
        """content

        The processed content info structure.
        """
        return self.get_content_info()

    def __repr__(self):
        return "<Manifest %r %r>" % (self.number, self.name)


@utils.decode_response
@utils.handle_http_errors
def create(resource, number, name, container, description=None, folder=None, attributes=None, content=None):
    """upload_content(resource, number, name, container, description, folder, attributes, content) -> new document

    Create a new `WTDocument`.

    The new document is created in the context of the `container` given.

    If `description` is used, then this string is set as the description of the
    new document.

    If `folder` is given, then it is deemed to be a *path* to a **existing** folder
    inside the `container` -- e.g something like `/Default/foo/bar/baz`.  Please note
    that the `/Default` part is mandatory.

    If `attributes` is given, then it is deemed to be a mapping of IBA values
    to be set on the new document.

    If `content` is given, then it is deemed to be a `content info` mapping which
    contains content to be set (upload) on the new document.
    See :py:func:`nexiles.tools.api.content.create_content_info`

    :param number:      the new number of the document
    :param name:        the new name of the document
    :param container:   the *name* of a container for the new document

    optional:

    :param folder:      the name of a folder inside the container
    :param description: the description of the new document
    :param content:     content info structure
    :param attributes:  a mapping of key/value pairs to be set as IBA attributes

    :returns: new business object iteration
    """
    info = {
            "number":    number,
            "name":      name,
            "container": container
    }

    if description:
        info["description"] = description

    if folder:
        info["folder"] = folder

    if attributes:
        info["attributes"] = attributes

    if content:
        info["content"] = content

    logger.debug("info: %r" % info)
    response = resource.post(info)
    logger.debug("post return: %r" % response)
    return response

@utils.decode_response
@utils.handle_http_errors
def delete(resource, oid):
    logger.debug("delete: oid=%s", oid)
    response = resource(oid).delete()
    logger.debug("delete return: %r", response)
    return response

######################################################################
######################################################################
######################################################################


def command_create(api, args):
    resource = get_resource(api, "documents")

    if args.manifest:
        mf = Manifest.from_file(args.manifest)
    else:
        mf = Manifest(**args.__dict__)

    doc = create(resource, mf.number, mf.name, mf.container,
            description=mf.description,
            folder=mf.folder,
            attributes=mf.attributes,
            content=mf.content)

    print "created: ", utils.object_pretty_print(doc)


def command_update(api, args):
    resource = get_resource(api, "documents")

    doc = utils.get_object(resource, args.oid)
    print "current iteration: ", utils.object_pretty_print(doc)

    if not utils.object_is_latest_iteration(resource, args.oid):
        raise RuntimeError("The business object at '%s' is not the latest iteration." % args.oid)

    if not args.iterate and not utils.object_is_checked_out(resource, args.oid):
        raise RuntimeError("The business object at '%s' is not checked out." % args.oid)

    raise NotImplementedError("content update not yet implemented")


def command_delete(api, args):
    resource = get_resource(api, "documents")

    doc = utils.get_object(resource, args.oid)
    print "current iteration: ", utils.object_pretty_print(doc)

    delete(resource, args.oid)
    print "deleted."


def add_commands(subparsers, defaults):
    def add_args(parser, update=False):
        parser.add_argument("--number",             required=False, dest="number", type=str, help="the number")
        parser.add_argument("--name",               required=False, dest="name", type=str, help="the name")
        if not update:
            parser.add_argument("--container-name", required=False, dest="container", type=str, help="the name of the container (Product, Library) for the document")
            parser.add_argument("--folder-path",    required=False, dest="folder", type=str, help="the folder path in the container to store the document")

        parser.add_argument("--description",        required=False, dest="description", type=str, help="the description")
        parser.add_argument("--manifest",           required=False, dest="manifest", type=str, help="read options from manifest JSON")
        return parser

    subparser = subparsers.add_parser("document-create")
    subparser = add_args(subparser)
    subparser.set_defaults(command=command_create)

    subparser = subparsers.add_parser("document-update")
    subparser = add_args(subparser, True)
    subparser.add_argument("--oid", required=True, dest="oid", type=validators.is_oid, help="the OID of the business object")
    subparser.set_defaults(command=command_update)

    subparser = subparsers.add_parser("document-delete")
    subparser.add_argument("--oid", required=True, dest="oid", type=validators.is_oid, help="the OID of the business object")
    subparser.set_defaults(command=command_delete)


# vim: set ft=python ts=4 sw=4 spell expandtab :
