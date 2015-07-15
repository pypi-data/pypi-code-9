from .interfaces import ISiteLogoSchema
from plone.app.layout.viewlets.common import ViewletBase
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.file import NamedImage
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class LogoViewlet(ViewletBase):

    def update(self):
        super(LogoViewlet, self).update()

        self.navigation_root_title = self.portal_state.navigation_root_title()
        logo_title = self.portal_state.portal_title()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISiteLogoSchema, prefix="plone")

        if getattr(settings, 'site_logo', False):
            filename, data = b64decode_file(settings.site_logo)
            data = NamedImage(data=data, filename=filename)
            width, height = data.getImageSize()
            img_src = '{}/@@site-logo/{}'.format(
                self.navigation_root_url, filename)
            self.logo_tag = u'<img src="{img_src}" '\
                u'width="{width}" height="{height}"'\
                u'alt="{logo_title}" title="{logo_title}"/>'.format(
                    img_src=img_src,
                    width=width,
                    height=height,
                    logo_title=logo_title
                )
        else:
            portal = self.portal_state.navigation_root()
            # Support for OFS.Image/skin layer based logos
            logo_name = 'logo.png'
            self.logo_tag = portal.restrictedTraverse(
                logo_name).tag(title=logo_title, alt=logo_title)
            # TODO: deprecate the skin layer based logo above and use one
            #       defined as browser or plone resource.
