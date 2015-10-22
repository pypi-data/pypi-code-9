# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse, reverse_lazy

from models import Entry, Blog

BLOG = Blog.objects.get_blog()


class BlogFeed(Feed):
	title = getattr(BLOG, 'title', '')
	link = reverse_lazy('luhublog-list')
	description = getattr(BLOG, 'tag_line', '')

	def items(self):
		return Entry.objects.all()

	def item_description(self, item):
		return item.lead_entry

	def item_title(self, item):
		return item.title

	def item_pubdate(self,item):
		return item.start_publication

	def item_link(self, item):
		return reverse('lihublog-detail', kwargs={'slug' : item.slug})

	def item_author_name(self, item):
		return item.author.full_name