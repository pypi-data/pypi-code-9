"""
Contains rich-text link handler definition.
"""
from django.utils.html import escape

from .models import Link


class LinkHandler(object):
    """
    LinkHandler will be invoked whenever we encounter an <a> element in HTML content
    with an attribute of data-linktype="link". The resulting element in the database
    representation will be: <a linktype="link" id="42">linked text</a>.
    """
    @staticmethod
    def get_db_attributes(tag):
        """
        Given an <a> tag that we've identified as a page link embed (because it has a
        data-linktype="link" attribute), return a dict of the attributes we should
        have on the resulting <a linktype="link"> element.

        :param tag: the tag dictionary.
        :rtype: dict.
        """
        return {'id': tag['data-id']}

    @staticmethod
    def expand_db_attributes(attrs, for_editor):
        """
        Given a dictionary of attributes, find the corresponding link instance and
        return its HTML representation.

        :param attrs: dictionary of link attributes.
        :param for_editor: whether or not HTML is for editor.
        :rtype: str.
        """
        try:
            editor_attrs    = ''
            link            = Link.objects.get(id=attrs['id'])

            if for_editor:
                editor_attrs = 'data-linktype="link" data-id="{0}" '.format(
                    link.id
                )

            return '<a {0}href="{1}" title="{2}">'.format(
                editor_attrs,
                escape(link.get_absolute_url()),
                link.title
            )
        except Link.DoesNotExist:
            return '<a>'
