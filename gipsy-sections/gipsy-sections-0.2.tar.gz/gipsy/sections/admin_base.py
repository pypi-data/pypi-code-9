#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.contrib import admin
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin
from django.contrib.contenttypes.admin import GenericStackedInline

from django.utils.translation import ugettext_lazy as _
from filebrowser.settings import ADMIN_THUMBNAIL


class SectionAdminMixin(object):

    sortable_field_name = 'order'
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

    extra = 0
    sortable_field_name = 'order'
    show_change_link = True

    related_lookup_fields = {
        'generic': [['content_type', 'object_id']],

    }

    fieldsets = ((
        _("Page"), {
            'fields': (
                ('title', ),
                ('description', ),
                ('image', ),
                ('content_type', 'object_id'),
                ('options', ),
                ('order', ),
                ('template_name', ),
            )
        }), (
        _("Activation"), {
            'classes': ('grp-collapse grp-closed',),
            'fields': (
                ('status', ),
                ('activate_date', 'deactivate_date'),
            )
        }))


class SectionInlineAdminBase(SectionAdminMixin, SuperInlineModelAdmin,
                             GenericStackedInline):
    ct_field = "section_content_type"
    ct_fk_field = "section_object_id"


class SectionAdminBase(SectionAdminMixin, SuperModelAdmin, admin.ModelAdmin):
    pass
