# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
import uuid
from logging import getLogger
import itertools
from zope.app.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue
from Acquisition import aq_inner, aq_parent
from zope.component import queryUtility, getUtility, getAdapter
import base64
from edeposit.policy import MessageFactory as _

from edeposit.content.amqp import IAMQPSender, IAMQPHandler
import json

logger = getLogger('edeposit.producent_wf_scripts')

# (occur-1 "def " nil (list (current-buffer)) "*Occur: producent_wf_scripts.py/def*")
# (occur-1 "class " nil (list (current-buffer)) "*Occur: producent_wf_scripts.py/class*")

def submitAgreementGeneration(wfStateInfo):
    producent = wfStateInfo.object
    getAdapter(producent,IAMQPSender,name="agreement-generate").send()
    pass

def ensureRolesConsistency(wfStateInfo):
    producent = wfStateInfo.object
    producent.ensureRolesConsistency()
    pass
