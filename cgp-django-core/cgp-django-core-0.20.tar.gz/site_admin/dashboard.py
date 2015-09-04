"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'ccl.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.modules import DashboardModule
from grappelli.dashboard.utils import get_admin_site_name

from .models import AdminLinkSet, AdminLinkItem, LegacyURL


import inspect
from django.conf import settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured
 
 
class DashboardLoaderModuleRegistry(object):
    CATEGORY_TOP = 'category_top'
    CATEGORY_COLUMN_ONE = 'category_column_one'
    CATEGORY_COLUMN_TWO = 'category_column_two'
    CATEGORY_COLUMN_THREE = 'category_column_three'
    CATEGORY_BOTTOM = 'category_bottom'

    CATEGORIES = [CATEGORY_TOP, CATEGORY_COLUMN_ONE, CATEGORY_COLUMN_TWO, 
        CATEGORY_COLUMN_THREE, CATEGORY_BOTTOM]


    def __init__(self):
        self._registry = {}
        for item in DashboardLoaderModuleRegistry.CATEGORIES:
            self._registry[item] = []

 
    def register(self, cateogry, title, url='', html=''):
        
        self._registry[cateogry].append({
            'title':title,
            'url':url,
            'html':html
        })

    @property
    def modules(self):
        return self._registry

    @property
    def top_modules(self):
        return self._registry[DashboardLoaderModuleRegistry.CATEGORY_TOP]

    @property
    def bottom_modules(self):
        return self._registry[DashboardLoaderModuleRegistry.CATEGORY_BOTTOM]

    @property
    def column_one_modules(self):
        return self._registry[DashboardLoaderModuleRegistry.CATEGORY_COLUMN_ONE]

    @property
    def column_two_modules(self):
        return self._registry[DashboardLoaderModuleRegistry.CATEGORY_COLUMN_TWO]

    @property
    def column_three_modules(self):
        return self._registry[DashboardLoaderModuleRegistry.CATEGORY_COLUMN_THREE]


dashboard_registry = DashboardLoaderModuleRegistry()
 

class AdminTasksDashboardModule(DashboardModule):

    title = 'Admin Tasks'
    template = 'admin/admin_tasks.html'
    
    

    def getActionMessage(self, item_count):
        if item_count == 0:
            return ""
        else:
            return "There are new admin tasks."

    
    def getVerbPhrase(self, count):
        if count >= 1:
            return str(count)
        else:
            return "No"

    def init_with_context(self, context):
        if self._initialized:
            return
        new_children = []
        
        unconnected_urls = LegacyURL.objects.needs_redirect()
        if len(unconnected_urls) > 0:
            new_children.append({
                'title': "There are %s urls to be redirected"%(self.getVerbPhrase(len(unconnected_urls))), 
                'url': "/admin/site_admin/legacyurl/?_redirect_path=0",
                "external":False,
            })

        total_count = len(unconnected_urls)

        self.admin_message = self.getActionMessage(total_count)
        self.children = new_children
        self._initialized = True


class AdminDashboard(Dashboard):

    # template = 'admin/custom_dashboard.html'
    class Media:
        js = (
            'admin/js/load_later.jqueryplugin.js',
            'admin/js/site_admin_dashboard.js',
        )
    

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # -- Django Admin
        self.children.append(modules.AppList(
            title=_('Applications'),
            column=1,
            collapsible=True,
            exclude=('django.contrib.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            title=_('Administration'),
            column=1,
            collapsible=True,
            models=('django.contrib.*',),
        ))     

        admin_link_sets = AdminLinkSet.objects.all()
        for link_set in admin_link_sets:

            children = []
            child_links = AdminLinkItem.objects.filter(parent=link_set)
            for child_link in child_links:
                children.append({
                    'title':child_link.title,
                    'url':child_link.url,
                    'external':False
                })

            # append another link list module for "support".
            self.children.append(modules.LinkList(
                link_set.title,
                column=2,
                children=children
            ))
        

        
        self.children.append(AdminTasksDashboardModule(

            _('Admin Tasks'),
            column=2,

        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))





