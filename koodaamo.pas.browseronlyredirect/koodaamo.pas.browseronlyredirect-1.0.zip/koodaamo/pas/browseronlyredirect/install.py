from AccessControl.Permissions import manage_users
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService import registerMultiPlugin

import plugin

manage_add_browseronlyredirect_form = PageTemplateFile('browser/add_plugin',
                            globals(), __name__='manage_add_browseronlyredirect_form' )


def manage_add_browseronlyredirect_helper( dispatcher, id, title=None, REQUEST=None ):
    """Add an browseronlyredirect Helper to the PluggableAuthentication Service."""

    sp = plugin.BrowseronlyredirectHelper( id, title )
    dispatcher._setObject( sp.getId(), sp )

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect( '%s/manage_workspace'
                                      '?manage_tabs_message='
                                      'browseronlyredirectHelper+added.'
                                      % dispatcher.absolute_url() )


def register_browseronlyredirect_plugin():
    try:
        registerMultiPlugin(plugin.BrowseronlyredirectHelper.meta_type)
    except RuntimeError:
        # make refresh users happy
        pass


def register_browseronlyredirect_plugin_class(context):
    context.registerClass(plugin.BrowseronlyredirectHelper,
                          permission = manage_users,
                          constructors = (manage_add_browseronlyredirect_form,
                                          manage_add_browseronlyredirect_helper),
                          visibility = None,
                          icon='browser/icon.gif'
                         )
