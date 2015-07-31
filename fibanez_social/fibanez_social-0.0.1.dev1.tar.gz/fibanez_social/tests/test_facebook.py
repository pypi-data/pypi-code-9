from django.test import TestCase

from fibanez_social.models.facebook import Facebook

class FacebookMethodTestCase(TestCase):
    
    def test_facebook_is_emtpy(self):
        """
        facebook_is_emtpy() should return []
        """
        self.assertEqual(Facebook.objects.exists(), False)
    