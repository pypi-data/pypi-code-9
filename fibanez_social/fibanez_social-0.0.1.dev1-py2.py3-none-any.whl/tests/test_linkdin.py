from django.test import TestCase

from fibanez_social.models.linkedin import Linkedin

class LinkdinMethodTestCase(TestCase):
    
    def test_linkedin_is_emtpy(self):
        """
        linkedin_is_emtpy() should return []
        """
        self.assertEqual(Linkedin.objects.exists(), False)
    