#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
This module does that.
"""
__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from django.contrib import admin
from filebrowser.settings import ADMIN_THUMBNAIL
from super_inlines.admin import SuperModelAdmin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

if 'django_mptt_admin' in settings.INSTALLED_APPS:
    from django_mptt_admin.admin import DjangoMpttAdmin as MPTTModelAdmin
else:
    from mptt.admin import MPTTModelAdmin


class PageAdminBase(MPTTModelAdmin, SuperModelAdmin, admin.ModelAdmin):

    show_change_link = True

    list_display = ('__str__', 'image_thumbnail')
    list_filter = ()
    search_fields = ('title', 'description', 'slug')
    date_hierarchy = 'created'
    save_as = True
    save_on_top = True
    actions_on_top = True
    actions_on_bottom = True

    # raw_id_fields = ('parent', )

    def image_thumbnail(self, obj):
        if obj.image and obj.image.filetype == "Image":
            url = obj.image.version_generate(ADMIN_THUMBNAIL).url
            return '<img src="{}" />'.format(url)
        else:
            return ""
    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = "Thumbnail"

    show_change_link = True

    related_lookup_fields = {
        'generic': [['content_type', 'object_id']],

    }

    prepopulated_fields = {"slug": ("title",)}

    readonly_fields = ('created', 'created_by', 'modified', 'modified_by')

    add_fieldsets = ((
        _("Page"), {
            'classes': ('wide',),
            'fields': (
                ('parent', ),
                ('title', ),
                ('slug', ),
                ('template_name', ),
            )
        }),
    )
    fieldsets = ((
        _("Page"), {
            'fields': (
                ('title', ),
                ('description', ),
                ('image', ),
                ('author', ),
            )
        }), (
        _("Placement"), {
            'fields': (
                ('parent',),
                ('slug',),
                ('template_name',),
            )
        }), (
        _("Activation"), {
            'classes': ('grp-collapse grp-closed',),
            'fields': (
                ('status', ),
                ('activate_date', 'deactivate_date'),
            )
        }), (
        _("Additional"), {
            'classes': ('grp-collapse grp-closed',),
            'fields': (
                ('options', ),
                ('content_type', 'object_id'),
            )
        }), (
        _("History"), {
            'classes': ('grp-collapse grp-closed',),
            'fields': (
                ('created', 'created_by', ),
                ('modified', 'modified_by', ),
            )
        })
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(PageAdminBase, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during object creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super(PageAdminBase, self).get_form(request, obj, **defaults)

    def response_add(self, request, obj, post_url_continue=None):
        if '_addanother' not in request.POST:
            request.POST['_continue'] = 1
        return super(PageAdminBase, self).response_add(request, obj,
                                                       post_url_continue)
