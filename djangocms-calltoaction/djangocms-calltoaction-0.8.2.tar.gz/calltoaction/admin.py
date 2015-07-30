from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import CallToActionRepository

from django.utils.text import Truncator
from django.utils.html import strip_tags


class CallToActionRepositoryAdmin(TranslatableAdmin, admin.ModelAdmin):
    list_display = ('code', 'style', 'image', 'display_content', 'display_link_text')

    def display_link_text(self, obj):
        return obj.link_text
    display_link_text.short_description = 'Link text'

    def display_content(self, obj):
        return strip_tags(Truncator(obj.content).words(5, html=True, truncate=' ...'))
    display_content.short_description = 'Content'


admin.site.register(CallToActionRepository, CallToActionRepositoryAdmin)
