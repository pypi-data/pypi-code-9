# coding=utf-8
__copyright__ = 'Copyright 2015, Abalt'

from oscar.apps.partner.admin import *  # noqa

from eurotaxes.partner.models import VATType, VATCountry


class VATTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'default')
    list_filter = ('default',)


class VATCountryAdmin(admin.ModelAdmin):
    list_display = ('country', 'vat_type', 'default', 'vat')
    list_filter = ('default',)


admin.site.register(VATType, VATTypeAdmin)
admin.site.register(VATCountry, VATCountryAdmin)
