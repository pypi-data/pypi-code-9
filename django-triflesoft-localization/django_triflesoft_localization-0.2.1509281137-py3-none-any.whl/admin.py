from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import site

from localization.models import Language


class LanguageAdmin(ModelAdmin):
    fieldsets = [
        ('Identity',   { 'classes': ('wide',), 'fields': [('id', 'code')]}),
        ('Value',      { 'classes': ('wide',), 'fields': [('name',)]}),
        ('Visibility', { 'classes': ('wide',), 'fields': [('is_published',)]}),
    ]
    list_display  = ['id', 'code', 'is_published']
    list_editable = [              'is_published']
    list_filter   = [              'is_published']
    ordering      = ['id', 'code', 'is_published']


site.register(Language, LanguageAdmin)
