from django.contrib.admin import ModelAdmin
from django.contrib.admin import StackedInline
from django.contrib.admin import TabularInline
from django.contrib.admin.sites import site
from django.forms import ModelForm
from django.forms.widgets import Textarea

from pages.models import Footer
from pages.models import Header
from pages.models import Menu
from pages.models import MenuPage
from pages.models import Page
from pages.models import PageContents
from pages.models import PageFooter
from pages.models import PageHeader
from pages.models import PageProperty
from pages.models import Property
from pages.models import Template


class PagePropertyInline(TabularInline):
    model = PageProperty
    extra = 1


class PageContentsForm(ModelForm):
    class Meta:
        model = PageContents
        exclude = []
        widgets = {
            'contents': Textarea( attrs={ 'rows': 80, 'cols': 160 } ),
        }


class PageContentsInline(StackedInline):
    model = PageContents
    extra = 1
    form = PageContentsForm


class PageFooterInline(TabularInline):
    model = PageFooter
    extra = 1


class PageHeaderInline(TabularInline):
    model = PageHeader
    extra = 1


class PropertyAdmin(ModelAdmin):
    fieldsets = [
        ('Identity', { 'classes': ('wide',), 'fields': [('code', 'name',)]}),
    ]
    list_display  = ['code', 'name']
    list_filter   = []
    ordering      = ['code', 'name']


class FooterForm(ModelForm):
    class Meta:
        model = Page
        exclude = []
        widgets = {
            'contents': Textarea( attrs={ 'rows': 40, 'cols': 160 } ),
        }


class FooterAdmin(ModelAdmin):
    fieldsets = [
        ('Identity', { 'classes': ('wide',), 'fields': [('code', 'name',)]}),
        ('Value',    { 'classes': ('wide',), 'fields': [('contents',)]}),
    ]
    list_display  = ['code', 'name']
    list_filter   = []
    ordering      = ['code', 'name']
    form = FooterForm


class HeaderForm(ModelForm):
    class Meta:
        model = Page
        exclude = []
        widgets = {
            'contents': Textarea( attrs={ 'rows': 40, 'cols': 160 } ),
        }


class HeaderAdmin(ModelAdmin):
    fieldsets = [
        ('Identity', { 'classes': ('wide',), 'fields': [('code', 'name',)]}),
        ('Value',    { 'classes': ('wide',), 'fields': [('contents',)]}),
    ]
    list_display  = ['code', 'name']
    list_filter   = []
    ordering      = ['code', 'name']
    form = HeaderForm


class MenuPageInline(TabularInline):
    model = MenuPage
    extra = 1


class MenuAdmin(ModelAdmin):
    inlines = [
        MenuPageInline
    ]
    fieldsets = [
        ('Identity', { 'classes': ('wide',), 'fields': [('code', 'name',)]}),
    ]
    list_display  = ['code', 'name']
    list_filter   = []
    ordering      = ['code', 'name']


class PageAdmin(ModelAdmin):
    inlines = [
        PageContentsInline,
        PageHeaderInline,
        PageFooterInline,
        PagePropertyInline
    ]
    fieldsets = [
        ('Identity',   { 'classes': ('wide',), 'fields': [('path',), ('url',)]}),
        ('Visibility', { 'classes': ('wide',), 'fields': [('is_published', 'template',)]}),
    ]
    list_display  = ['path', 'template', 'is_published']
    list_editable = [                    'is_published']
    list_filter   = ['path', 'template', 'is_published']
    ordering      = ['path']

    class Media:
        css = {
            'all': ('/static/admin/css/textarea-font.css', '/static/admin/css/inline-collapse.css',)
        }
        js = ('/static/admin/js/textarea-tab.js',)


class TemplateAdmin(ModelAdmin):
    fieldsets = [
        ('Identity', { 'classes': ('wide',), 'fields': [('code', 'name', )]}),
        ('Value',    { 'classes': ('wide',), 'fields': [('path',)]}),
    ]
    list_display  = ['code', 'name', 'path']
    list_filter   = []
    ordering      = ['path']


site.register(Footer,   FooterAdmin)
site.register(Header,   HeaderAdmin)
site.register(Menu,     MenuAdmin)
site.register(Page,     PageAdmin)
site.register(Property, PropertyAdmin)
site.register(Template, TemplateAdmin)
