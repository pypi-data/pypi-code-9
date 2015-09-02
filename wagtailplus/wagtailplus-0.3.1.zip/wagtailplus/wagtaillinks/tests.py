"""
Contains application unit tests.
"""
from wagtailplus.utils.views import tests
from .models import Link


class TestLinkIndexView(tests.BaseTestIndexView):
    url_namespace   = 'wagtaillinks'
    template_dir    = 'wagtaillinks/links'

    def _create_sequential_instance(self, index):
        """
        Creates sequential link instances.

        :param index: the sequential index to use.
        """
        Link.objects.create(
            link_type       = Link.LINK_TYPE_EXTERNAL,
            title           = 'Link #{0}'.format(index),
            external_url    = 'http://www.site-{0}.com'.format(index)
        )

class TestLinkCreateView(tests.BaseTestCreateView):
    url_namespace   = 'wagtaillinks'
    template_dir    = 'wagtaillinks/links'
    model_class     = Link
    filter_keys     = ['title']

    def _get_post_data(self):
        """
        Stub method for extending class to return data dictionary
        to create a new model instance on POST.

        :rtype: dict.
        """
        return {
            'link_type':    Link.LINK_TYPE_EXTERNAL,
            'title':        'Test Link',
            'external_url': 'http://www.test.com'
        }

class TestLinkUpdateView(tests.BaseTestUpdateView):
    url_namespace   = 'wagtaillinks'
    template_dir    = 'wagtaillinks/links'
    model_class     = Link

    def _get_instance(self):
        """
        Stub method for extending class to return saved model class
        instance.

        :rtype: django.db.models.Model.
        """
        return Link.objects.create(
            link_type       = Link.LINK_TYPE_EXTERNAL,
            title           = 'Test Link',
            external_url    = 'http://www.test.com'
        )

    def _get_post_data(self):
        """
        Stub method for extending class to return data dictionary
        to create a new model instance on POST.

        :rtype: dict.
        """
        return {
            'link_type':    Link.LINK_TYPE_EXTERNAL,
            'title':        'Test Link Changed',
            'external_url': 'http://www.test.com'
        }

class TestLinkDeleteView(tests.BaseTestDeleteView):
    url_namespace   = 'wagtaillinks'
    template_dir    = 'wagtaillinks/links'
    model_class     = Link

    def _get_instance(self):
        """
        Stub method for extending class to return saved model class
        instance.

        :rtype: django.db.models.Model.
        """
        return Link.objects.create(
            link_type       = Link.LINK_TYPE_EXTERNAL,
            title           = 'Test Link',
            external_url    = 'http://www.test.com'
        )