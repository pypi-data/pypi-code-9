##############################################################################
#
# Copyright (c) 2009 Projekt01 GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id:$
"""
__docformat__ = "reStructuredText"


import zope.interface
import zope.schema
import zope.interface.common.interfaces


class IResourceNotFound(zope.interface.common.interfaces.IException):
    """NotFound error for resources

    NOTE: this NotFound allows to register a custom NotFound page whcih is
    able to render a 500 status without to invoke the default NotFound page
    including the html layout.

    NOTE: this interface is not inherited from INotFound or ITraversalException
    because we need to prevent that we will get the default INotFound or
    ITraversalException page.
    """


class IResourceManager(zope.interface.Interface):
    """Content delivery network resource manager

    The resource manager knows the resource output path during extraction.
    The resource manager is also used for generate the right url as an adapter
    adapting the resource layer (request).

    The p01.recipe.cdn package is able to extract the cdn resources. See:
    p01.recipe.cdn for more information.
    """

    rawURI = zope.schema.ASCIILine(
        title=u'Raw resource base uri including fomratting arguments',
        description=u'Raw resource base uri including fomratting arguments',
        default='',
        required=False)

    uri = zope.schema.ASCIILine(
        title=u'Formatted resource base uri',
        description=u'Formatted resource base uri',
        default=None,
        required=False)

    version = zope.schema.ASCIILine(
        title=u'Resource manger version',
        description=u'Resource manger version',
        required=True)

    # optional uri substitution arguments
    namespace = zope.schema.ASCIILine(
        title=u'Resource manager namespace',
        description=u'Resource manager namespace',
        default='',
        required=False)

    skin = zope.schema.ASCIILine(
        title=u'Skin name',
        description=u'Skin name',
        default='',
        required=False)

    site = zope.schema.ASCIILine(
        title=u'Site name',
        description=u'Site name',
        default='',
        required=False)

    pkgVersion = zope.schema.TextLine(
        title=u'Package version (only available for resources from eggs)',
        description=u'Package version (only available for resources from eggs)',
        required=False)

    useSVNVersions = zope.schema.Bool(
        title=u"Use svn version per file (don't enable on extraction)",
        description=u"Use svn version per file (don't enable on extraction)",
        default=False,
        required=False)

    svnVersionSourcePath = zope.schema.ASCIILine(
        title=u'Generated cdn.json resource version source map path',
        description=u'Generated cdn.json resource version source map path',
        required=False)

    zrtReplaces = zope.schema.Text(
        title=u'Generated zrt-replace.less content',
        description=u'Generated zrt-replace.less content',
        default=u'',
        required=False)

    zrtDirReplaces = zope.schema.Text(
        title=u'Generated zrt-replace.less content (directory first)',
        description=u'Generated zrt-replace.less content (directory first)',
        default=u'',
        required=False)

    svnZRTReplacePath = zope.schema.ASCIILine(
        title=u'Generated zrt-replace.less file path',
        description=u'Generated zrt-replace.less file path',
        required=False)

    versions = zope.schema.Dict(
        title=u'File name (svn) version mapping',
        description=u'File name (svn) version mapping',
        required=False)

    # Note, this output is optional and only required for resource extraction
    # If this output is None, the p01.recipe.cdn recipe option ``output`` is
    # used.
    # See p01.recipe.cdn extract.py for more information
    # Note: if `the recipe output option is used, the namespace will get
    # ignored
    output = zope.schema.ASCIILine(
        title=u'Resource extract output dir path',
        description=u'Resource extract output dir path',
        default=None,
        required=False)

    def getURI(name=None):
        """Build the correct url based on the uri, namespace and version and
        resource name.

        We also, allow to use * as a version manager marker.

        An initial devmode uri could look like:

        http://localhost:8080/++skin++Admin/%(version)s/@@

        If your applicaiton uses site and subsite and each sub site is useing
        another resource manager, the relative subsite path could get used
        as namespace. Then you uri could look like:

        http://localhost:8080/++skin++Admin/%(namespace)s/%(version)s/@@

        And the sub site could be set to something like: "root/subsite"

        A production setup does not require any special uri setup in general.
        It fully depends on your web servers rewrite rule and your extracted
        resource location. You will probably use a sub domain like:

        http://%(namespace)s.foobar.com/%(version)s/@@

        or with an additional namespace:

        http://cdn.foobar.com/%(namespace)s/%(version)s/@@

        or just as minimal as possible

        http://cdn.foobar.com/%(version)s/@@

        """


class ICDNResource(zope.interface.Interface):
    """Content delivery network (cdn) resource.

    This offload resource allows us to configure resources with custom urls.
    This is used if you like to offload static resources form the zope and
    it's fornt end proxy server. Each off load resource contains it's own url
    which can point to another subdomain.

    Note, take care if you use SSL, make sure that you use a wildcard
    certificate which is valid for different subdomains. This is a new kind of
    certificate which only some certificate seller offer. One of such a seller
    is www.godaddy.com. Take care and don't get confused, normaly a wildcard
    certificate is only valid for one domain but for more then one server IP
    address.
    """


class IZRTCDNResource(ICDNResource):
    """CDN zrt resource."""


class II18nCDNResource(ICDNResource):
    """CDN i18n resource."""


class ICDNResourceDirectory(ICDNResource):
    """CDN resource directory."""
