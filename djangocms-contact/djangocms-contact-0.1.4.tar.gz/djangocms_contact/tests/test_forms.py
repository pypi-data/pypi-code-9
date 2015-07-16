from django.test import TestCase
from djangocms_contact.forms import ContactForm


class ContactFormTest(TestCase):

    def test_form_validation(self):
        form = ContactForm({
            'name': 'name',
            'email': 'email@example.com',
            'subject': 'subject',
            'message': 'message'
        })
        self.assertTrue(form.is_valid())
