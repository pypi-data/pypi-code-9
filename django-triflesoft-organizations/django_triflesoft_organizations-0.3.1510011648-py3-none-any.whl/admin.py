from django.contrib.admin import ModelAdmin
from django.contrib.admin import TabularInline
from django.contrib.admin.sites import site

from organizations.models import Branch
from organizations.models import BranchAddress
from organizations.models import BranchCode
from organizations.models import BranchContact
from organizations.models import BranchName
from organizations.models import BranchSchedule
from organizations.models import ContactType
from organizations.models import ContactTypeName
from organizations.models import Organization
from organizations.models import OrganizationCode
from organizations.models import OrganizationContact
from organizations.models import OrganizationName
from organizations.models import OrganizationType
from organizations.models import OrganizationTypeName


class ContactTypeNameInline(TabularInline):
    model = ContactTypeName
    extra = 1


class ContactTypeAdmin(ModelAdmin):
    inlines = [
        ContactTypeNameInline,
    ]
    fieldsets = [
        ('Identity',   {'classes': ('wide',), 'fields': [('code',), ]}),
    ]
    list_display  = ['code']
    list_editable = []
    list_filter   = []
    ordering      = ['code']


class OrganizationTypeNameInline(TabularInline):
    model = OrganizationTypeName
    extra = 1


class OrganizationTypeAdmin(ModelAdmin):
    inlines = [
        OrganizationTypeNameInline,
    ]
    fieldsets = [
        ('Identity',   {'classes': ('wide',), 'fields': [('code',), ]}),
        ('Visibility', {'classes': ('wide',), 'fields': [('is_published'), ]}),
    ]
    list_display  = ['code', 'is_published']
    list_editable = [        'is_published']
    list_filter   = []
    ordering      = ['code', 'is_published']


class OrganizationCodeInline(TabularInline):
    model = OrganizationCode
    extra = 1


class OrganizationNameInline(TabularInline):
    model = OrganizationName
    extra = 1


class OrganizationContactInline(TabularInline):
    model = OrganizationContact
    extra = 1


class OrganizationAdmin(ModelAdmin):
    inlines = [
        OrganizationCodeInline,
        OrganizationNameInline,
        OrganizationContactInline
    ]
    fieldsets = [
        ('Identity',   {'classes': ('wide',), 'fields': [('id', 'country', 'region'), ('code', 'type'), ]}),
        ('Visibility', {'classes': ('wide',), 'fields': [('is_published'), ]}),
    ]
    list_display  = ['code', 'name', 'country', 'region', 'type', 'is_published']
    list_editable = [                                             'is_published']
    list_filter   = [                'country', 'region', 'type', 'is_published']
    ordering      = ['code']


class BranchCodeInline(TabularInline):
    model = BranchCode
    extra = 1


class BranchNameInline(TabularInline):
    model = BranchName
    extra = 1


class BranchContactInline(TabularInline):
    model = BranchContact
    extra = 1


class BranchAddressInline(TabularInline):
    model = BranchAddress
    extra = 1


class BranchScheduleInline(TabularInline):
    model = BranchSchedule
    extra = 1


class BranchAdmin(ModelAdmin):
    inlines = [
        BranchCodeInline,
        BranchNameInline,
        BranchContactInline,
        BranchAddressInline,
        BranchScheduleInline,
    ]
    fieldsets = [
        ('Identity',   {'classes': ('wide',), 'fields': [('code', 'organization', 'region'), ]}),
        ('Visibility', {'classes': ('wide',), 'fields': [('is_published'), ]}),
        ('Value',      {'classes': ('wide',), 'fields': [('latitude', 'longitude'), ]}),
    ]
    list_display  = ['code', 'name', 'organization', 'region', 'is_published', 'latitude', 'longitude']
    list_editable = [                                          'is_published']
    list_filter   = [                'organization', 'region', 'is_published']
    ordering      = ['code']


site.register(ContactType,      ContactTypeAdmin)
site.register(OrganizationType, OrganizationTypeAdmin)
site.register(Organization,     OrganizationAdmin)
site.register(Branch,           BranchAdmin)
