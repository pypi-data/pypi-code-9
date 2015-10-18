# -*- coding: utf-8 -*-

from django.contrib import admin

from writeback.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('date_created', )


admin.site.register(Message, MessageAdmin)
