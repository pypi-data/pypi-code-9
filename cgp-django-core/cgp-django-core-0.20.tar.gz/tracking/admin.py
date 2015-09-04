from django.contrib import admin

from .models import *


class EventAdmin(admin.ModelAdmin):

    list_display = ['created', 'full_url', 'domain', 'path', 'category',
        'action','label', 'value']

    list_filter = ('full_url', 'domain', 'path', 'category', 'action',
        'label', 'created')
    search_fields = ('full_url','domain','path', 'category', 'action',
        'label', 'value', 'content', 'user_agent')
    
    fields = ['created', 'full_url', 'domain', 'path', 'category',
        'action','label', 'value', 'content', 'user_agent']
    csv_fields = list_display

    readonly_fields = ('created',)

admin.site.register(Event, EventAdmin)