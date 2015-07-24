from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from cms.test_utils.testcases import CMSTestCase


class ContactViewTests(CMSTestCase):

    @override_settings(ROOT_URLCONF='djangocms_contact.tests.urls')
    def test_post_form_submit(self):
        data = {
            'name': 'name',
            'email': 'email@example.com',
            'subject': 'subject',
            'message': 'message'
        }
        test_url = reverse('djangocms_contact:contact')
        resp1 = self.client.post(test_url, data)
        resp2 = self.client.post(test_url, {})
        self.assertEqual(resp1.status_code, 302)
        self.assertEqual(resp2.status_code, 400)
