from django.contrib.admin import ModelAdmin
from django.contrib.admin import TabularInline
from django.contrib.admin.sites import site

from locations.models import Country
from locations.models import CountryName
from locations.models import Region
from locations.models import RegionName


class CountryNameInline(TabularInline):
    model = CountryName
    extra = 1


class CountryAdmin(ModelAdmin):
    inlines = [
        CountryNameInline,
    ]
    fieldsets = [
        ('Identity',   {'classes': ('wide',), 'fields': [('id', 'code',), ]}),
        ('Visibility', {'classes': ('wide',), 'fields': [('is_published',), ]}),
    ]
    list_display  = ['id', 'code', 'name', 'is_published']
    list_editable = [                      'is_published']
    ordering      = ['id', 'code',         'is_published']


class RegionNameInline(TabularInline):
    model = RegionName
    extra = 1


class RegionAdmin(ModelAdmin):
    inlines = [
        RegionNameInline,
    ]
    fieldsets = [
        ('Identity',   {'classes': ('wide',), 'fields': [('id', 'country', 'code'), ]}),
        ('Visibility', {'classes': ('wide',), 'fields': [('is_published',), ]}),
        ('Value',      {'classes': ('wide',), 'fields': [('time_zone',), ]}),
    ]
    list_display  = ['id', 'country', 'code', 'name', 'is_published', 'time_zone']
    list_editable = [                                 'is_published']
    ordering      = ['id', 'country', 'code',         'is_published', 'time_zone']


site.register(Country, CountryAdmin)
site.register(Region,  RegionAdmin)
