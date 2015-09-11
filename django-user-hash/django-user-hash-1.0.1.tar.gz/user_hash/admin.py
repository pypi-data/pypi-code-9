# coding=utf-8
from django.contrib import admin
from user_hash.models import UserHash

__author__ = 'franki'


class UserHashAdmin(admin.ModelAdmin):
    list_display = ['created', 'user', 'hash', 'key', 'value', 'expires', ]
    readonly_fields = list_display


admin.site.register(UserHash, UserHashAdmin)
