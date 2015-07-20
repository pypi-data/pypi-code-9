# -*- coding: utf-8 -*-

import logging
import datetime
import DateTime

import simplejson as json

from zope import interface
from zope import component

from plone import api

from plone.dexterity.schema import SCHEMA_CACHE
from plone.dexterity.interfaces import IDexterityContent

from Products.CMFCore.interfaces import ISiteRoot
from Products.ZCatalog.interfaces import ICatalogBrain
from Products.ATContentTypes.interfaces import IATContentType

from plone.jsonapi.routes.interfaces import IInfo
from plone.jsonapi.routes.interfaces import IDataManager

__author__ = 'Ramon Bartl <ramon.bartl@googlemail.com>'
__docformat__ = 'plaintext'


logger = logging.getLogger("plone.jsonapi.routes")


class Base(object):
    """ Base Adapter
    """
    interface.implements(IInfo)

    def __init__(self, context):
        self.context = context
        self.keys = []

        # additional attributes to extract besides the Schema keys
        self.attributes = {
            "id":          "getId",
            "uid":         "UID",
            "title":       "Title",
            "description": "Description",
            "created":     "created",
            "modified":    "modified",
            "effective":   "effective",
            "portal_type": "portal_type",
            "tags":        "Subject",
        }

    def to_dict(self):
        data = to_dict(self.context, keys=self.keys)
        for key, attr in self.attributes.iteritems():
            if data.get(key):
                continue  # don't overwrite
            value = getattr(self.context, attr, None)
            if callable(value):
                value = value()
            data[key] = get_json_value(self.context, key, value=value)
        return data

    def __call__(self):
        return self.to_dict()


class ZCDataProvider(Base):
    """ Catalog Brain Adapter
    """
    interface.implements(IInfo)
    component.adapts(ICatalogBrain)

    def __init__(self, context):
        super(ZCDataProvider, self).__init__(context)

    def to_dict(self):
        brain = self.context
        return {
            "id":          brain.getId,
            "uid":         brain.UID,
            "title":       brain.Title,
            "description": brain.Description,
            "url":         brain.getURL(),
            "portal_type": brain.portal_type,
            "created":     brain.created.ISO8601(),
            "modified":    brain.modified.ISO8601(),
            "effective":   brain.effective.ISO8601(),
            "type":        brain.portal_type,
            "tags":        brain.Subject,
        }


class DexterityDataProvider(Base):
    """ Data Provider for Dexterity based content types
    """
    interface.implements(IInfo)
    component.adapts(IDexterityContent)

    def __init__(self, context):
        super(DexterityDataProvider, self).__init__(context)

        schema = SCHEMA_CACHE.get(context.portal_type)
        self.keys = schema.names()


class ATDataProvider(Base):
    """ Archetypes Adapter
    """
    interface.implements(IInfo)
    component.adapts(IATContentType)

    def __init__(self, context):
        super(ATDataProvider, self).__init__(context)
        schema = context.Schema()
        self.keys = schema.keys()


class SiteRootDataProvider(Base):
    """ Site Root Adapter
    """
    interface.implements(IInfo)
    component.adapts(ISiteRoot)

    def __init__(self, context):
        super(SiteRootDataProvider, self).__init__(context)


# ---------------------------------------------------------------------------
#   Functional Helpers
# ---------------------------------------------------------------------------

def to_dict(obj, keys):
    """ returns a dictionary of the given keys
    """
    out = dict()
    # see interfaces.IDataManager
    dm = IDataManager(obj)
    for key in keys:
        value = dm.get(key)
        out[key] = get_json_value(obj, key, value=value)
    if out.get("workflow_info"):
        logger.warn("Workflow Info ommitted since the key 'workflow_info' "
                    "was found in the current schema")
        return out
    wf_info = get_wf_info(obj)
    out["workflow_info"] = wf_info
    out["state"] = wf_info.get("status")
    return out


def get_json_value(obj, key, value=None):
    """ json save value encoding
    """

    # extract the value from the object if omitted
    if value is None:
        value = IDataManager(obj).get(key)

    # known date types
    date_types = (datetime.datetime,
                  datetime.date,
                  DateTime.DateTime)

    # check if we have a date
    if isinstance(value, date_types):
        return get_iso_date(value)

    # check if the value is a file object
    if hasattr(value, "filename"):
        # => value is e.g. a named blob file
        return get_file_dict(obj, key, value=value)

    if not is_json_serializable(value):
        return None

    return value


def get_file_dict(obj, key, value=None):
    """ file representation of the given data
    """

    # extract the value from the object if omitted
    if value is None:
        value = IDataManager(obj).get(key)

    # extract file attributes
    data = value.data.encode("base64")
    content_type = get_content_type(value)
    filename = getattr(value, "filename", "")
    download = None

    if IDexterityContent.providedBy(obj):
        # calculate the download url
        download = "{}/@@download/{}/{}".format(
            obj.absolute_url(), key, filename)
    else:
        # calculate the download url
        download = "{}/download".format(obj.absolute_url())

    return {
        "data": data,
        "size": len(value.data),
        "content_type": content_type,
        "filename": filename,
        "download": download,
    }


def get_content_type(fileobj):
    """ get the content type of the file object
    """
    if hasattr(fileobj, "contentType"):
        return fileobj.contentType
    return getattr(fileobj, "content_type", "application/octet-stream")


def get_iso_date(date=None):
    """ get the iso string for python datetime objects
    """
    if date is None:
        return ""

    if isinstance(date, (DateTime.DateTime)):
        return date.ISO8601()

    return date.isoformat()


def is_json_serializable(thing):
    """ checks if the given thing can be serialized to json
    """
    try:
        json.dumps(thing)
        return True
    except TypeError:
        return False


def get_wf_info(obj):
    """ returns the workflow information of the first assigned workflow
    """

    # get the portal workflow tool
    wf_tool = api.portal.get_tool("portal_workflow")

    # the assigned workflows of this object
    wfs = wf_tool.getWorkflowsFor(obj)

    # no worfkflows assigned -> return
    if not wfs:
        return {}

    # get the first one
    workflow = wfs[0]

    # get the status info of the current state (dictionary)
    status = wf_tool.getStatusOf(workflow.getId(), obj)

    # https://github.com/collective/plone.jsonapi.routes/issues/33
    if not status:
        return {}

    # get the current review_status
    current_state_id = status.get("review_state", None)

    # get the wf status object
    current_status = workflow.states[current_state_id]

    # get the title of the current status
    current_state_title = current_status.title

    # get the transition informations
    transitions = map(to_transition_info, wf_tool.getTransitionsFor(obj))

    return {
        "workflow":     workflow.getId(),
        "status":       current_state_title,
        "review_state": current_state_id,
        "transitions":  transitions
    }


def to_transition_info(transition):
    """ return the transition information
    """
    return {
        "value":   transition["id"],
        "display": transition["description"],
        "url":     transition["url"],
    }
