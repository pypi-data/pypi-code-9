class RootShortcut(object):
    """Provides shortcut to the root folder"""

    # This time we don't bother with i18n and assume
    # the whole world understands English
    title = u'Root'

    # Portal root relative path
    link = "/"

    def render(self, context):

        portal_state = context.restrictedTraverse('@@plone_portal_state')

        return ["""
        <img src="img/folder.png" />
        <a id="root_folder" href="%s">%s</a>
        """ % (portal_state.portal_url() + self.link, self.title)]
