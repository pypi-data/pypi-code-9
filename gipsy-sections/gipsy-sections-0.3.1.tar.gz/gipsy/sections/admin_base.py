#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

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


class SectionInlineAdminBase(SectionAdminMixin, GenericTabularInline):
    ct_field = "section_content_type"
    ct_fk_field = "section_object_id"

    readonly_fields = ('edit_link', )

    fieldsets = ((
        None, {
            'fields': (
                ('template_name', ),
                ('title', ),
                ('status', ),
                ('order', ),
                ('edit_link', ),
            )
        }), )

    def edit_link(self, obj):
        if obj:
            return """<a href="/admin/sections/section/{}/">edit</a>
        """.format(obj.pk)
    edit_link.allow_tags = True
    edit_link.short_description = 'edit'


class SectionAdminBase(SectionAdminMixin, admin.ModelAdmin):

    add_fieldsets = ((
        None, {
            'classes': ('wide',),
            'fields': (
                ('section_content_type', 'section_object_id'),
                ('template_name', ),
                ('title', ),
            )
        }),
    )
    fieldsets = ((
        None, {
            'classes': ('wide',),
            'fields': (
                ('section_content_type', 'section_object_id'),
                ('template_name', ),
                ('title', ),
                ('description', ),
                ('image', ),
                ('content_type', 'object_id'),
                ('options', ),
                ('order', ),
            )
        }), (
        _("Activation"), {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': (
                ('status', ),
                ('activate_date', 'deactivate_date'),
            )
        }))

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(SectionAdminBase, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during object creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super(SectionAdminBase, self).get_form(request, obj, **defaults)

    def response_add(self, request, obj, post_url_continue=None):
        if '_addanother' not in request.POST:
            request.POST['_continue'] = 1
        return super(SectionAdminBase, self).response_add(request, obj,
                                                          post_url_continue)
