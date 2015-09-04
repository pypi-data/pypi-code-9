from django.conf import settings
from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin.util import flatten_fieldsets
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib import messages

from .models import *


def resave_item(modeladmin, request, queryset):	

	items_saved = 0
	save_errors = 0
	for item in queryset:
	    try:
	    	item.save()
	    	items_saved += 1
	    except:
	    	save_errors += 1

	if items_saved > 0:
	 	messages.success(request, '%s items were saved.'%(items_saved))

	if save_errors > 0:
		messages.warning(request, '%s items were not saved.'%(save_errors))

resave_item.short_description = "Re-Save Item"

def attempt_to_redirect(self, request, queryset):
	count = 0
	for page in queryset:
		#attempt_to_redirect_link(page)
		print count
		count += 1

	messages.success(request, u'%s Links(s) attempted to be redirected '%(count))

class HasRedirectFilterSpec(SimpleListFilter):
	title = u'Has Redirect Path'
	parameter_name = u'_redirect_path'

	def lookups(self, request, model_admin):
		return (
			('1', _('Has Redirect'), ),
			('0', _('Needs Redirect'), ),
		)

	def queryset(self, request, queryset):
		kwargs = {
		'%s'%self.parameter_name : None,
		}
		if self.value() == '0':
			return queryset.filter( Q(_redirect_path__isnull=True) | Q(_redirect_path='') )  
		if self.value() == '1':
			return queryset.exclude( Q(_redirect_path__isnull=True) | Q(_redirect_path='') )
			
		return queryset


class AdminLinkItemAdmin(admin.TabularInline):

	model = AdminLinkItem
	ordering = ("order",)
	sortable_field_name = 'order'
	extra = 0
	fieldsets = (
		( 'Links', { 'fields': ( 'order', 'title', 'url', ) } ),
	)
	
	inline_classes = ('grp-collapse grp-open',)


class AdminLinkSetAdmin(admin.ModelAdmin):
	

	fieldsets = (
		( 'Link Set', { 'fields': ( 'title',) } ),
	)
	list_display = ( 'title', 'order' )
	search_fields = ("title", )
	list_editable = ('order',)
	csv_fields = flatten_fieldsets(fieldsets)

	inlines = [AdminLinkItemAdmin]

 
class LegacyURLRefererItemAdmin(admin.TabularInline):

	def visit(self, obj):

		return "<a href='%s' target='_blank'>Visit</a>"%(obj.referer_url)
	visit.allow_tags = True

	fk_name = "legacy_url"
	model = LegacyURLReferer
	extra = 0
	fieldsets = (
		( 'Links', { 'fields': ( 'visit', 'referer_title', 'referer_url', 'created', 'modified') } ),
	)   
	readonly_fields = ('created', 'modified', 'visit')


class LegacyURLAdmin(admin.ModelAdmin):
	
	
	def visit_old_link(self, obj):
		return "<a href='%s%s' target='_blank'>Visit Legacy Link</a>"%(settings.LEGACY_URL_ARCHIVE_DOMAIN, obj.url)
	visit_old_link.allow_tags = True

	def redirect_link(self, obj):
		url = obj._redirect_path
		if url:
			return "<a href='%s' target='_blank'>%s</a>"%(url, url)
		else:
			return "No redirect"
	redirect_link.allow_tags = True

	def test_redirect(self, obj):
		return "<a href='/%s' target='_blank'>Test Redirect</a>"%(obj.url)
	test_redirect.allow_tags = True

	class Media:
		js = [
			'%sadmin/js/related_lookup_fix.js' % settings.STATIC_URL
		]

	fieldsets = (
		( 'Link Set', { 'fields': ( 'title', 'url', '_redirect_path', 'redirect_to_url', 'content_type', 'object_id', 'test_redirect', 'visit_old_link','created', 'modified') } ),
	)
	list_display = ( 'pk','title', 'url',  'redirect_to_url',  'content_type', 'object_id', 'redirect_link', 'test_redirect',  'visit_old_link', )
	list_display_links = ('pk','title','url')
	search_fields = ("title", "url")

	readonly_fields = ('pk','created', 'modified', '_redirect_path', 'visit_old_link', 'test_redirect')
	list_editable = ('redirect_to_url','content_type', 'object_id',  )

	list_filter =  (HasRedirectFilterSpec,)

	csv_fields = ('url', 'title', '_redirect_path', 'redirect_to_url', 'content_type', 'object_id',)

	autocomplete_lookup_fields = {
		'generic': [['content_type', 'object_id'],],
	}
	csv_fields = flatten_fieldsets(fieldsets)

	actions = []
	inlines = [LegacyURLRefererItemAdmin]



admin.site.register(AdminLinkSet, AdminLinkSetAdmin)
admin.site.register(LegacyURL, LegacyURLAdmin)