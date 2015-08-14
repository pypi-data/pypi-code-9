#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

if 'django_mptt_admin' in settings.INSTALLED_APPS:
    from django_mptt_admin.admin import DjangoMpttAdmin as MPTTModelAdmin
else:
    from mptt.admin import MPTTModelAdmin


class MenuNodeAdminMixin(object):
    show_change_link = True
    # list_display = ('__str__', 'url', 'content_object')
    list_filter = ()
    search_fields = ('title', 'description', 'slug')
    date_hierarchy = 'created'
    save_as = True
    save_on_top = True
    actions_on_top = True
    actions_on_bottom = True
    extra = 0
    show_change_link = True
    tree_auto_open = 1

    related_lookup_fields = {
        'generic': [['content_type', 'object_id']],

    }

    fieldset_base = (
        _("Menu node"), {
            'fields': (
                ('title', ),
                ('parent', 'stub'),
            )
        })
    fieldset_link = (
        _("Link"), {
            'fields': (
                ('url', ),
                ('content_type', 'object_id'),
            )
        })
    fieldset_activation = (
        _("Activation"), {
            'classes': ('grp-collapse grp-closed',),
            'fields': (
                ('status', ),
                ('activate_date', 'deactivate_date'),
            )
        })
    fieldset_additional = (
        _("Additional"), {
            'classes': ('grp-collapse grp-closed',),
            'fields': (
                ('description', ),
                ('options', ),
            )
        })
    fieldsets = (
        fieldset_base,
        fieldset_link,
        fieldset_activation,
        fieldset_additional,
    )


class MenuNodeInlineAdminBase(MenuNodeAdminMixin, admin.TabularInline):
    fieldsets = (
        (_("Menu node"), {
            'fields': (
                ('title', ),
            )
        }),
        MenuNodeAdminMixin.fieldset_link,
        (_("Edit"), {
            'fields': (
                ('edit_link', ),
            )
        }),
    )
    readonly_fields = ('edit_link', )

    def edit_link(self, obj):
        url = '#'
        if obj.pk:
            info = self.model._meta.app_label, self.model._meta.model_name
            url = reverse('admin:%s_%s_change' % info, args=(obj.pk,))
        return '<a href="{}">edit</a>'.format(url)
    edit_link.short_description = _("Edit link")
    edit_link.allow_tags = True


class MenuNodeAdminBase(MenuNodeAdminMixin, MPTTModelAdmin):
    pass
