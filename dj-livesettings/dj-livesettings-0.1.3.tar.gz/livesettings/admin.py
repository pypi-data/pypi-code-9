# coding: utf-8

from django.contrib import admin

from .forms import LiveSettingsForm
from .models import LiveSetting


class LiveSettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'key_type', 'value')
    form = LiveSettingsForm


admin.site.register(LiveSetting, LiveSettingsAdmin)
