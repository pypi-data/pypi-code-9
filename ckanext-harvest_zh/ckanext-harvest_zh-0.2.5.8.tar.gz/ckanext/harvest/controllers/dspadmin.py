# coding=utf-8

__author__ = 'nispc'

import ckan.plugins.toolkit as toolkit

from ckan.plugins.toolkit import BaseController
from ckan.plugins.toolkit import c
from ckan.plugins.toolkit import _

class DSPAdminController(BaseController):
    def config(self):

        #在「/ckan-admin/dsp-integrate」頁面render之前，先確認使用者是否為sysadmin。

        context = {'model': c.model,
                   'user': c.user, 'auth_user_obj': c.userobj}
        try:
            toolkit.check_access('sysadmin', context, {})
        except toolkit.NotAuthorized:
            toolkit.abort(401, _('Need to be system administrator to administer') )
        c.revision_change_state_allowed = True

        return toolkit.render('admin/sync.html')