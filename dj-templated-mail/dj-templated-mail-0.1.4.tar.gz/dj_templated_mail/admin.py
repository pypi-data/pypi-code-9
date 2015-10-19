# coding: utf-8

from django.contrib import admin
from .models import EmailTemplate


class EmailTemplateAdmin(admin.ModelAdmin):
    actions = ['duplicate']
    list_display = ('template_name', 'subject',)

    def duplicate(self, request, queryset):
        for t in queryset:
            t.pk = None
            t.save()


admin.site.register(EmailTemplate, EmailTemplateAdmin)
