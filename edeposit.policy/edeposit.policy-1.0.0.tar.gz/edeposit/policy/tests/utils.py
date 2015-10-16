from functools import wraps
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from AccessControl.Permission import getPermissions

def getContentType(portal, contenttype):
    portal_types=portal.get('portal_types')
    #portal_types.listContentTypes()
    fti = portal_types[contenttype]
    return fti

def getUserPermissions(portal, username, context):
    mt = portal['portal_membership']
    user = mt.getMemberById(username)
    permissions = [pp[0] for pp in getPermissions() if user.checkPermission(pp[0],context)]
    return permissions

def withPortal(f):
    @wraps(f)
    def wrapper(self, **kwargs):
        if 'portal' not in kwargs:
            kwargs['portal'] = self.layer['portal']
        f(self, **kwargs)
    return wrapper

def withProducentFolder(f):
    @withPortal
    @wraps(f)
    def wrapper(self, **kwargs):
        portal = kwargs['portal']
        if 'producentFolder' not in kwargs:
            setRoles(portal, TEST_USER_ID, ('Manager',))
            portal.invokeFactory('edeposit.user.producentfolder', 'edlf1', title=u"E-Deposit Library Folder")
            kwargs['producentFolder'] = portal['edlf1']
        f(self, **kwargs)
    return wrapper

def withProducent(f):
    @withProducentFolder
    @wraps(f)
    def wrapper(self,  **kwargs):
        producentFolder = kwargs['producentFolder']
        if 'producent' not in kwargs:
            producentFolder.invokeFactory('edeposit.user.producent', 'producent', title=u"E-Deposit Producent")
            kwargs['producent'] = producentFolder['producent']
            kwargs['producent'].manage_setLocalRoles(TEST_USER_ID, ('E-Deposit: Assigned Producent',))
        f(self, **kwargs)
    return wrapper
