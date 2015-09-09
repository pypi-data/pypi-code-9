from django.contrib import admin

from textplusstuff.admin import TextPlusStuffRegisteredModelAdmin

from .models import ContentGroup, Content


class ContentInline(admin.StackedInline):
    model = Content
    extra = 0
    ordering = ['order']


class ContentGroupAdmin(TextPlusStuffRegisteredModelAdmin):
    inlines = [ContentInline]


admin.site.register(ContentGroup, ContentGroupAdmin)
