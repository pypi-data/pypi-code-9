# -*- coding: utf-8 -*-
from edeposit.policy import MessageFactory as _
from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer

def createFolders(portal):
    # import sys,pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    # Factory-type information id is the same as in types.xml
    # optionally you can set checkConstraints=False to skip permission
    # checks
    if 'producents' not in portal.objectIds():
        portal.invokeFactory('edeposit.user.producentfolder', 'producents', title=u"Producenti")
        #portal.invokeFactory('Document', 'uvodni', title=u"Uvodni strana")
    pass

def setupVarious(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile('edeposit.user.marker.txt') is None:
        # Not your add-on
        return
    portal = context.getSite()
    createFolders(portal)
