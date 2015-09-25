"""
Contains application administration.
"""
from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Category


class CategoryAdmin(TreeAdmin):
    form            = movenodeform_factory(Category)
    list_display    = ('name', 'depth', 'total',)
    fields          = (
        'name',
        '_position',
        '_ref_node_id',
    )

admin.site.register(Category, CategoryAdmin)
