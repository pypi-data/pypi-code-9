##
## setuphandlers.py
##
## Copyright (C) 2008, 2013 Uli Fouquet
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""Setup psj extensions.
"""
import transaction
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO

PRODUCT_DEPENDENCIES = ()


def registerTransform(site, out, name, module):
    transforms = getToolByName(site, 'portal_transforms')
    if name in transforms:
        unregisterTransform(site, out, name)
    transforms.manage_addTransform(name, module)
    print >> out, "Registered transform", name
    return


def unregisterTransform(site, out, name):
    transforms = getToolByName(site, 'portal_transforms')
    try:
        transforms.unregisterTransform(name)
        print >> out, "Removed transform", name
    except AttributeError:
        print >> out, "Could not remove transform", name, "(not found)"
    return


def register_products(site, out, reinstall=False):
    quickinstaller = getToolByName(site, 'portal_quickinstaller')
    for product in PRODUCT_DEPENDENCIES:
        if reinstall and quickinstaller.isProductInstalled(product):
            quickinstaller.reinstallProducts([product])
            transaction.savepoint()
        elif not quickinstaller.isProductInstalled(product):
            quickinstaller.installProducts([product])
            transaction.savepoint()
    return


def install(site):
    """Install psj stuff.
    """
    out = StringIO()

    # Register transforms
    for name, module in [
        ('odt_to_html', 'psj.policy.transforms.odt_to_html'),
        ('odt_to_pdf', 'psj.policy.transforms.odt_to_pdf'),
        ('doc_to_html', 'psj.policy.transforms.doc_to_html'),
        ('doc_to_pdf', 'psj.policy.transforms.doc_to_pdf'),
        ]:
        print >> out, "Installing %s transform" % name
        registerTransform(site, out, name, module)
    # Reregister standard transformations, so that they appear in the
    # list of transforms _after_ ours.
    unregisterTransform(site, out, 'word_to_html')
    registerTransform(site, out, 'word_to_html',
                      'Products.PortalTransforms.transforms.word_to_html')

    # Register additional products
    register_products(site, out)
    return out.getvalue()


def uninstall(site):
    """Uninstall psj stuff.
    """
    out = StringIO()

    # Remove transforms
    unregisterTransform(site, out, 'odt_to_html')
    unregisterTransform(site, out, 'odt_to_pdf')
    unregisterTransform(site, out, 'doc_to_html')
    unregisterTransform(site, out, 'doc_to_pdf')
    return out.getvalue()


def setupPSJTransforms(context):
    """
    Setup PortalTransforms step.
    """
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('portal-transforms-various.txt') is None:
        return
    site = context.getSite()
    #installPSJTransforms(site)
    install(site)


def setupPSJSite(context):
    # Only run step if a flag file is present (e.g. not an extension profile)
    #if context.readDataFile('portal-transforms-various.txt') is None:
    #    return
    site = context.getSite()
    install(site)
