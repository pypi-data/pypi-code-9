from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from models import Author, Entry, EntryCategory, Blog, TwitterCard, OpenGraph, BlogSocialMedia


class TwitterCardInline(GenericStackedInline):
	model = TwitterCard
	max_num = 1


class OpenGraphInline(GenericStackedInline):
	model = OpenGraph
	max_num = 1

class BlogSocialMediaInline(admin.StackedInline):
	model = BlogSocialMedia
	max_num = 1

@admin.register(Blog)
class BlogAdmin( admin.ModelAdmin ):
	list_display = ('title', 'site',)
	inlines = [TwitterCardInline, OpenGraphInline, BlogSocialMediaInline]

@admin.register(Author)
class AuthorAdmin( admin.ModelAdmin ):
	list_display = ('user', 'full_name')
	
@admin.register(EntryCategory)
class EntryCategoryAdmin( admin.ModelAdmin ):
	list_display = ('name', 'blog',)
	
@admin.register(Entry)
class EntryAdmin( admin.ModelAdmin ):
	list_display = ('title', 'author', 'category', 'blog', 'status', )
	inlines = [TwitterCardInline, OpenGraphInline,]
	prepopulated_fields = {'slug': ('title',), }
	fieldsets = (
		(None, {
			'fields' : ('status', 'category', 'author')
		}),
		('Entrada', {
			'fields' : ('title', 'lead_entry', 'image_header', 'image_caption', 'content', 'related')
		}),
		('SEO', {
			'fields' : ('slug', 'seo_title', 'seo_description', 'seo_keywords')
		})
	)

	def get_queryset(self, request):
		return self.model.default.all()