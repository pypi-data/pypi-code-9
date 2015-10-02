"""
Contains application chooser view definitions.
"""
import json

from django.core.urlresolvers import reverse

from wagtailplus.utils.views import chooser


class LinkChooser(chooser.ChooserView):
    def get_json(self, link):
        """
        Returns specified link instance as JSON.

        :param link: the link instance.
        :rtype: JSON.
        """
        return json.dumps({
            'id':           link.id,
            'title':        link.title,
            'url':          link.get_absolute_url(),
            'edit_link':    reverse(
                '{0}:edit'.format(self.url_namespace),
                kwargs = {'pk': link.pk}
            ),
        })

LinkChosen = chooser.chosen_view_factory(LinkChooser)
