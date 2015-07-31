from django.test import TestCase

from fibanez_social.models.twitter import Twitter

class TwitterMethodTestCase(TestCase):
    
    def test_twitter_is_emtpy(self):
        """
        twitter_is_emtpy() should return []
        """
        self.assertEqual(Twitter.objects.exists(), False)
    