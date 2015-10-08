__author__ = 'vinay'
from django.contrib import admin

from .models import Content, Category


class CmsPageCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CmsPageCategoryAdmin)


class ContentAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'publish', 'status')
    list_filter = ('publish', 'category', 'status')
    search_fields = ('title', 'url', 'template')
    readonly_fields = ('created_on', 'modified_on')

admin.site.register(Content, ContentAdmin)
