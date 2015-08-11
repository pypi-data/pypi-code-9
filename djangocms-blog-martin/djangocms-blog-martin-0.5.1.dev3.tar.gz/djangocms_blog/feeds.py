# -*- coding: utf-8 -*-
from urlparse import urljoin
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.templatetags.static import static
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _

from .models import Post
from .settings import get_setting
from .cms_helpers import render_placeholderfield

from bs4 import BeautifulSoup


def get_full_site_uri():
    site = "".join((settings.SITE_PROTOCOL, Site.objects.get_current().domain))
    return site


def clean_html(input):
    site = get_full_site_uri()
    soup = BeautifulSoup(input, 'html.parser')

    # Fix images so they contain the full url in src
    for img in soup.find_all('img'):
        img.attrs['src'] = '%s' % (urljoin(site, img.attrs['src']))

    # Remove \n

    return str(soup)

class CustomFeed(Rss201rev2Feed):

    def rss_attributes(self):
        attrs = super(CustomFeed, self).rss_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        return attrs

    def add_root_elements(self, handler):
        super(CustomFeed, self).add_root_elements(handler)
        handler.startElement(u'image', {})
        handler.addQuickElement(u"url", self.feed['image_url'])
        handler.addQuickElement(u"title", self.feed['title'])
        handler.addQuickElement(u"link", self.feed['link'])
        handler.endElement(u'image')

    def add_item_elements(self, handler, item):
        # Invoke this same method of the super-class to add the standard elements
        # to the 'item's.
        super(CustomFeed, self).add_item_elements(handler, item)

        # Add a new custom element named 'content' to each of the tag 'item'.
        handler.addQuickElement(u"content:encoded", item['content'])


class MyFeed(Feed):
    feed_type = CustomFeed

    def link(self):
        return reverse('djangocms_blog:posts-latest')

    def title(self):
        return settings.DJANGOCMS_BLOG_TITLE

    def items(self, obj=None):
        return Post.objects.published().order_by('-date_published')[:10]
        # return Post.objects.published().order_by('date_published')[:2]

    def item_title(self, item):
        return item.safe_translation_getter('title')

    def item_description(self, item):
        # Here we remove html and whitespace. Or not.
        description_image = '<img src="%s" alt="%s" width="100%%">' % (item.get_image_full_url(), item.main_image.default_alt_text)

        return "%s%s" % (description_image, item.safe_translation_getter('abstract'))

    def item_pubdate(self, item):
        return item.date_published

    author_name = settings.DJANGOCMS_BLOG_AUTHOR_NAME

    author_email = settings.DJANGOCMS_BLOG_AUTHOR_EMAIL

    def item_author_name(self, item):
        return item.get_author_name()

    def item_author_email(self, item):
        return item.author.email

    def item_extra_kwargs(self, item):
        """
        Returns an extra keyword arguments dictionary that is used with
        the `add_item` call of the feed generator.
        Add the 'content' field of the 'Entry' item, to be used by the custom feed generator.
        """
        content = render_placeholderfield(item.content)
        return {
            'content': clean_html(content),
        }

    def feed_extra_kwargs(self, obj):
        return {'image_url': urljoin(get_full_site_uri(), static(settings.DJANGOCMS_BLOG_IMAGE))}


# from django.contrib.sites.models import Site
# from django.contrib.syndication.views import Feed
# from django.core.urlresolvers import reverse
# from django.utils.translation import ugettext as _

# from .models import Post


# class LatestEntriesFeed(Feed):

#     def link(self):
#         return reverse('djangocms_blog:posts-latest')

#     def title(self):
#         return _('Blog articles on %(site_name)s') % {'site_name': Site.objects.get_current().name}

#     def items(self, obj=None):
#         return Post.objects.published().order_by('-date_published')[:10]

#     def item_title(self, item):
#         return item.safe_translation_getter('title')

#     def item_description(self, item):
#         return item.safe_translation_getter('abstract')


class TagFeed(MyFeed):

    def get_object(self, request, tag):
        return tag  # pragma: no cover

    def items(self, obj=None):
        return Post.objects.published().filter(tags__slug=obj)[:10]
