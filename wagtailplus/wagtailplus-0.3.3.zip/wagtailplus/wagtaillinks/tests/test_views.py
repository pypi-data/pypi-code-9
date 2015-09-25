"""
Contains view unit tests.
"""
from django.core.urlresolvers import reverse

from wagtailplus.tests import views
from ..models import Link


class TestLinkIndexView(views.BaseTestIndexView):
    url_namespace   = 'wagtaillinks'
    template_dir    = 'wagtaillinks/links'

    def _create_sequential_instance(self, index):
        Link.objects.create(
            link_type       = Link.LINK_TYPE_EXTERNAL,
            title           = 'Link #{0}'.format(index),
            external_url    = 'http://www.site-{0}.com'.format(index)
        )

class TestLinkCreateView(views.BaseTestCreateView):
    url_namespace   = 'wagtaillinks'
    template_dir    = 'wagtaillinks/links'
    model_class     = Link
    filter_keys     = ['title']

    def _get_post_data(self):
        return {
            'link_type':    Link.LINK_TYPE_EXTERNAL,
            'title':        'Test Link',
            'external_url': 'http://www.test.com/'
        }

class TestLinkUpdateView(views.BaseTestUpdateView):
    url_namespace   = 'wagtaillinks'
    template_dir    = 'wagtaillinks/links'
    model_class     = Link

    def _get_instance(self):
        return Link.objects.create(
            link_type       = Link.LINK_TYPE_EXTERNAL,
            title           = 'Test Link',
            external_url    = 'http://www.test.com/'
        )

    def _get_post_data(self):
        return {
            'link_type':    Link.LINK_TYPE_EXTERNAL,
            'title':        'Test Link Changed',
            'external_url': 'http://www.test.com/'
        }

class TestLinkDeleteView(views.BaseTestDeleteView):
    url_namespace   = 'wagtaillinks'
    template_dir    = 'wagtaillinks/links'
    model_class     = Link

    def _get_instance(self):
        return Link.objects.create(
            link_type       = Link.LINK_TYPE_EXTERNAL,
            title           = 'Test Link',
            external_url    = 'http://www.test.com/'
        )

class TestEmailLinkChooserView(views.BaseTestChooserView):
    url_namespace   = 'wagtaillinks'
    template_dir    = 'wagtaillinks/chooser'
    model_class     = Link

    def _create_sequential_instance(self, index):
        return Link.objects.create(
            link_type   = Link.LINK_TYPE_EMAIL,
            title       = 'Test Email #{0}'.format(index),
            email       = 'somebody-{0}@something.com'.format(index)
        )

    def get(self, params=None):
        if not params:
            params = {}

        return self.client.get(
            reverse('wagtailadmin_choose_page_email_link'),
            params
        )

class TestExternalLinkChooserView(views.BaseTestChooserView):
    url_namespace   = 'wagtaillinks'
    template_dir    = 'wagtaillinks/chooser'
    model_class     = Link

    def _create_sequential_instance(self, index):
        return Link.objects.create(
            link_type       = Link.LINK_TYPE_EXTERNAL,
            title           = 'Test Link #{0}'.format(index),
            external_url    = 'http://www.site-{0}.com'.format(index)
        )

    def get(self, params=None):
        if not params:
            params = {}

        return self.client.get(
            reverse('wagtailadmin_choose_page_external_link'),
            params
        )

class TestEmailLinkChosenView(views.BaseTestChosenView):
    url_namespace   = 'wagtaillinks'
    template_dir    = 'wagtaillinks/chooser'
    model_class     = Link

    def _get_instance(self):
        return Link.objects.create(
            link_type   = Link.LINK_TYPE_EMAIL,
            title       = 'Test Email',
            email       = 'somebody@something.com'
        )

class TestExternalLinkChosenView(views.BaseTestChosenView):
    url_namespace   = 'wagtaillinks'
    template_dir    = 'wagtaillinks/chooser'
    model_class     = Link

    def _get_instance(self):
        return Link.objects.create(
            link_type       = Link.LINK_TYPE_EXTERNAL,
            title           = 'Test Link',
            external_url    = 'http://www.test.com/'
        )

class TestChooserCreateEmailLinkView(views.BaseTestChooserCreateView):
    url_namespace   = 'wagtaillinks'
    template_dir    = 'wagtaillinks/chooser'
    model_class     = Link

    def _get_post_data(self):
        return {
            'link_type':    Link.LINK_TYPE_EMAIL,
            'title':        'Test Email',
            'email':        'somebody@something.com',
        }

    def test_get(self):
        # Generate the response.
        response = self.client.get(
            reverse('wagtailadmin_choose_page_email_link')
        )

        # Check assertions.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            '{0}/chooser.html'.format(self.template_dir)
        )
        self.assertTemplateUsed(
            response,
            '{0}/results.html'.format(self.template_dir)
        )
        self.assertTemplateUsed(
            response,
            '{0}/chooser.js'.format(self.template_dir)
        )

    def test_post(self):
        # Get POST data.
        data = self._get_post_data()

        # Generate the response.
        response = self.client.post(
            reverse('wagtailadmin_choose_page_email_link'),
            data
        )

        # Check assertions.
        self.assertTemplateUsed(
            response,
            '{0}/chosen.js'.format(self.template_dir)
        )
        self.assertContains(
            response,
            'modal.respond'
        )
        self.assertTrue(
            self.model_class.objects.filter(**data).exists()
        )

class TestChooserCreateExternalLinkView(views.BaseTestChooserCreateView):
    url_namespace   = 'wagtaillinks'
    template_dir    = 'wagtaillinks/chooser'
    model_class     = Link

    def _get_post_data(self):
        return {
            'link_type':    Link.LINK_TYPE_EXTERNAL,
            'title':        'Test Link',
            'external_url': 'http://www.test.com/',
        }

    def test_get(self):
        # Generate the response.
        response = self.client.get(
            reverse('wagtailadmin_choose_page_external_link')
        )

        # Check assertions.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            '{0}/chooser.html'.format(self.template_dir)
        )
        self.assertTemplateUsed(
            response,
            '{0}/results.html'.format(self.template_dir)
        )
        self.assertTemplateUsed(
            response,
            '{0}/chooser.js'.format(self.template_dir)
        )

    def test_post(self):
        # Get POST data.
        data = self._get_post_data()

        # Generate the response.
        response = self.client.post(
            reverse('wagtailadmin_choose_page_external_link'),
            data
        )

        # Check assertions.
        self.assertTemplateUsed(
            response,
            '{0}/chosen.js'.format(self.template_dir)
        )
        self.assertContains(
            response,
            'modal.respond'
        )
        self.assertTrue(
            self.model_class.objects.filter(**data).exists()
        )
