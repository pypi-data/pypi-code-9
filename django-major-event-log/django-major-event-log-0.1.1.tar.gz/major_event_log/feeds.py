"""Creates the Atom feed for the major PREMIS events."""

from django.utils.feedgenerator import Atom1Feed, rfc3339_date
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.paginator import Paginator, InvalidPage
from django.contrib.syndication.views import Feed
from django.http import Http404

from .models import Event


class PaginatedAtom1FeedMixin(object):
    """Mixin to enable pagination for feeds using Atom1Feed"""

    def _create_link_attr(self, rel, page):
        """Helper function to compose the attributes dictionary argument
        that handler.addQuickElement accepts.
        """
        href = u'{0}?{1}={2}'.format(
            self.feed['link'], self.feed['page_field'], page)

        return {u'rel': rel, u'href': href}

    def add_root_elements(self, handler):
        """This method overrides the Atom1Feed.add_root_elements
        in order to place the additional link elements into the
        desired location in the document.
        """
        handler.addQuickElement('title', self.feed['title'])

        if self.feed['feed_url'] is not None:
            handler.addQuickElement(
                u'link',
                '',
                self._create_link_attr(u'self', self.feed['cr_page'])
            )

        handler.addQuickElement(
            u'link', '', self._create_link_attr(u'first', 1))

        handler.addQuickElement(
            u'link',
            '',
            self._create_link_attr(u'last', self.feed['last_page'])
        )

        if self.feed.get('prev_page', None) is not None:
            handler.addQuickElement(
                u'link',
                '',
                self._create_link_attr(u'previous', self.feed['prev_page'])
            )

        if self.feed.get('next_page', None) is not None:
            handler.addQuickElement(
                u'link',
                '',
                self._create_link_attr(u'next', self.feed['next_page'])
            )

        handler.addQuickElement('id', self.feed['id'])
        handler.addQuickElement(
            'updated', rfc3339_date(self.latest_post_date()))

        if self.feed['author_name'] is not None:
            handler.startElement('author', {})
            handler.addQuickElement('name', self.feed['author_name'])

            if self.feed['author_email'] is not None:
                handler.addQuickElement('email', self.feed['author_email'])

            if self.feed['author_link'] is not None:
                handler.addQuickElement('uri', self.feed['author_link'])

            handler.endElement('author')

        if self.feed['subtitle'] is not None:
            handler.addQuickElement('subtitle', self.feed['subtitle'])

        for cat in self.feed['categories']:
            handler.addQuickElement('category', '', {'term': cat})

        if self.feed['feed_copyright'] is not None:
            handler.addQuickElement('rights', self.feed['feed_copyright'])


class MajorEventLogFeed(PaginatedAtom1FeedMixin, Atom1Feed):
    """Custom Atom Feed for Event objects.

    The only changes between this custom feed and the base Atom Feed
    are that this feed specifies its mime_type as 'application/xml',
    pagination is added, and the 'alternate' link is removed.
    """

    mime_type = 'application/xml'


class PaginatedFeedMixin(object):
    """Feed mixin to enable pagination."""

    paginator = None
    page = 1
    items_per_page = 10
    page_field = 'page'

    def setup_paginator(self, request, items):
        """Instantiates the paginator object and attaches
        it to self.

        This needs to be called from `get_object` in order to receive
        the request object.
        """
        self.page = request.GET.get(self.page_field, 1)
        self.paginator = Paginator(items, self.items_per_page)

    def get_current_page(self):
        """Get the current page of the Paginator."""
        try:
            return self.paginator.page(self.page)
        except InvalidPage:
            raise Http404("Invalid page number.")

    def get_page_kwargs(self):
        """Returns the keyword arguments for the page links.

        This is intended to be called from `feed_extra_kwargs`.
        """
        page = self.get_current_page()
        kwargs = {}

        kwargs.setdefault('page_field', self.page_field)
        if page.has_next():
            kwargs.setdefault('next_page', page.next_page_number())

        if page.has_previous():
            kwargs.setdefault('prev_page', page.previous_page_number())

        kwargs.setdefault('last_page', str(self.paginator.num_pages))
        kwargs.setdefault('cr_page', page.number)

        return kwargs


class LatestEventsFeed(PaginatedFeedMixin, Feed):
    feed_type = MajorEventLogFeed
    title = 'PREMIS Major Event Log'
    link = reverse_lazy('major-event-log:feed')
    author_name = 'Major Event Log'
    author_link = 'http://digital2.library.unt.edu/name/nm0005293/'
    page_field = 'p'

    def get_object(self, request):
        events = Event.objects.order_by('-entry_created')
        self.setup_paginator(request, events)
        return events

    def feed_extra_kwargs(self, display):
        return self.get_page_kwargs()

    def items(self, obj):
        return self.get_current_page().object_list

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.detail

    def item_link(self, item):
        return reverse('major-event-log:event_details', args=[item.pk])

    def item_updateddate(self, item):
        return item.entry_modified
