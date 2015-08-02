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
        }))
