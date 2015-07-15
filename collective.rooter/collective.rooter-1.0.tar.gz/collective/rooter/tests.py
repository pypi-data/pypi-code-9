from Products.CMFCore.utils import getToolByName
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from collective.rooter import getNavigationRoot
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.uuid.utils import uuidToObject
from plone.uuid.interfaces import IUUID
from zope.app.publication.interfaces import BeforeTraverseEvent
from zope.event import notify
from zope.interface import alsoProvides
import unittest


@onsetup
def setup_package():
    fiveconfigure.debug_mode = True
    import collective.rooter
    zcml.load_config('configure.zcml', collective.rooter)
    fiveconfigure.debug_mode = False

setup_package()
ptc.setupPloneSite()


class IntegrationTests(ptc.PloneTestCase):

    def test_search_root(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Folder', 'site1')
        alsoProvides(self.portal.site1, INavigationRoot)

        self.portal.invokeFactory('Document', 'd1')
        self.portal.site1.invokeFactory('Document', 'd2')

        catalog = getToolByName(self.portal, 'portal_catalog')

        lazy = catalog(portal_type='Document')
        results = [x.getId for x in lazy]
        self.failUnless('d1' in results)
        self.failUnless('d2' in results)

        # Simulate traversal
        notify(BeforeTraverseEvent(self.portal.site1, self.portal.REQUEST))

        root = getNavigationRoot()
        self.assertEquals(
            root.absolute_url(),
            self.portal.site1.absolute_url())

        lazy = catalog(portal_type='Document')
        results = [x.getId for x in lazy]
        self.failIf('d1' in results)
        self.failUnless('d2' in results)

    def test_search_root_with_explicit_path(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Folder', 'site1')
        alsoProvides(self.portal.site1, INavigationRoot)

        self.portal.invokeFactory('Document', 'd1')
        self.portal.site1.invokeFactory('Document', 'd2')

        catalog = getToolByName(self.portal, 'portal_catalog')

        lazy = catalog(portal_type='Document',
                       path='/'.join(self.portal.getPhysicalPath()))
        results = [x.getId for x in lazy]
        self.failUnless('d1' in results)
        self.failUnless('d2' in results)

        # Simulate traversal
        notify(BeforeTraverseEvent(self.portal.site1, self.portal.REQUEST))

        lazy = catalog(portal_type='Document',
                       path='/'.join(self.portal.getPhysicalPath()))
        results = [x.getId for x in lazy]
        self.failUnless('d1' in results)
        self.failUnless('d2' in results)

    def test_get_obj_by_uuid(self):
        """uuidToObject should also return objects from other subsites, if the
        UUID is known and permissions allow to.
        """
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Folder', 'site1')
        alsoProvides(self.portal.site1, INavigationRoot)

        self.portal.invokeFactory('Document', 'd1')
        d1 = self.portal['d1']

        # Simulate traversal
        notify(BeforeTraverseEvent(self.portal.site1, self.portal.REQUEST))

        root = getNavigationRoot()
        self.assertEquals(
            root.absolute_url(),
            self.portal.site1.absolute_url())

        self.assertEqual(uuidToObject(IUUID(d1)), d1)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IntegrationTests))
    return suite
