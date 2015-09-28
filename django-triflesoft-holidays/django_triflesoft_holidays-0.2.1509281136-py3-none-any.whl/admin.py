from django.contrib.admin import ModelAdmin
from django.contrib.admin import TabularInline
from django.contrib.admin.sites import site

from holidays.models import Holiday
from holidays.models import HolidayException
from holidays.models import HolidayName


class HolidayNameInline(TabularInline):
    model = HolidayName
    extra = 1


class HolidayExceptionInline(TabularInline):
    model = HolidayException
    extra = 1


class HolidayAdmin(ModelAdmin):
    inlines = [
        HolidayNameInline,
        HolidayExceptionInline,
    ]
    fieldsets = [
        ('Identity', {'classes': ('wide',), 'fields': [('country', 'code',)]}),
        ('Value',    {'classes': ('wide',), 'fields': [('recurrent_month', 'recurrent_day',)]}),
    ]
    list_display  = ['code', 'name', 'country', 'recurrent_month', 'recurrent_day']
    list_editable = []
    ordering      = ['code',         'country', 'recurrent_month', 'recurrent_day']


site.register(Holiday, HolidayAdmin)
