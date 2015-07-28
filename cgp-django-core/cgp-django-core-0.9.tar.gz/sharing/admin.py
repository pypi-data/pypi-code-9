from django.contrib import admin

from .models import *

class SocialShareLinkInline(admin.TabularInline):
    model = SocialShareLink 
    extra = 0
    sortable_field_name = "order"

class SocialShareSettingsAdmin(admin.ModelAdmin):
    inlines = [SocialShareLinkInline]

    list_display = ('title', 'site',)
    readonly_fields = ('title',)
    list_filter = ('site',)

admin.site.register(SocialShareSettings, SocialShareSettingsAdmin)