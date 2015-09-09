from __future__ import unicode_literals
import json

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stacks_contentgroup.models import ContentGroup


class StacksContentGroupTestCase(TestCase):
    """The test suite for stacks-contentgroup."""

    fixtures = ['stackscontentgroup.json']
    maxDiff = None

    def setUp(self):
        """Set up the test suite."""
        password = '12345'
        user = User.objects.create_user(
            username='test_user',
            email='user@test.com',
            password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        user_client = Client()
        user_login = user_client.login(
            username='test_user',
            password=password
        )
        self.assertTrue(user_login)
        self.user = user
        self.user_client = user_client
        self.contentgroup = ContentGroup.objects.get()

    def test_instance(self):
        """Test the test StacksContentGroup instance."""
        self.assertEqual(
            self.contentgroup.pk,
            1
        )
        self.assertEqual(
            self.contentgroup.__str__(),
            'Sesame Street Characters'
        )
        self.assertEqual(
            self.contentgroup.content_set.all()[0].__str__(),
            'Sesame Street Characters - #1. Big Bird'
        )

    def test_list_serialization(self):
        """Test the StacksImageList textplusstuff serializer."""
        response = self.client.get(
            '/textplusstuff/stacks_contentgroup/'
            'contentgroup/detail/1/'
        )
        self.assertEqual(
            response.status_code,
            200
        )
        self.assertEqual(
            json.loads(response.content)['context'],
            {
                "name": "Sesame Street Characters",
                "display_title": "Sesame Street Characters",
                "extra_context": {},
                "content": [
                    {
                        "id": "sesame-street-characters-1-1",
                        "title": "Big Bird",
                        "menu_image": {
                            "square_crop": (
                                "/media/__sized__/content-group/big-bird-crop-"
                                "c0-47__0-2-490x490.jpg"
                            )
                        },
                        "alternate_menu_image": {},
                        "content": {
                            "as_plaintext": (
                                "Big Bird is a character on the children's "
                                "television show Sesame Street. Officially "
                                "performed by Caroll Spinney since 1969, he "
                                "is an eight-foot two-inch (249 cm) tall "
                                "bright primrose-yellow bird.\n"
                            ),
                            "as_html": (
                                "<p>Big Bird is a character on the children's "
                                "television show Sesame Street. Officially "
                                "performed by Caroll Spinney since 1969, he "
                                "is an eight-foot two-inch (249 cm) tall "
                                "bright primrose-yellow bird.</p>\n"
                            ),
                            "raw_text": (
                                "Big Bird is a character on the children's "
                                "television show Sesame Street. Officially "
                                "performed by Caroll Spinney since 1969, he "
                                "is an eight-foot two-inch (249 cm) tall "
                                "bright primrose-yellow bird."
                            ),
                            "as_html_no_tokens": (
                                "<p>Big Bird is a character on the children's "
                                "television show Sesame Street. Officially "
                                "performed by Caroll Spinney since 1969, he "
                                "is an eight-foot two-inch (249 cm) tall "
                                "bright primrose-yellow bird.</p>\n"
                            ),
                            "as_markdown": (
                                "Big Bird is a character on the children's "
                                "television show Sesame Street. Officially "
                                "performed by Caroll Spinney since 1969, he "
                                "is an eight-foot two-inch (249 cm) tall "
                                "bright primrose-yellow bird."
                            )
                        }
                    },
                    {
                        "id": "sesame-street-characters-1-2",
                        "title": "Cookie Monster",
                        "menu_image": {
                            "square_crop": (
                                "/media/__sized__/content-group/cookie-monster"
                                "-crop-c0-47__0-23-490x490.jpg"
                            )
                        },
                        "alternate_menu_image": {},
                        "content": {
                            "as_plaintext": (
                                "Cookie Monster is a Muppet on the long "
                                "running children's television show Sesame "
                                "Street. He is best known for his voracious "
                                "appetite and his famous eating phrases: \"Me "
                                "want cookie!\", \"Me eat cookie!\", and \"Om "
                                "nom nom nom\" (said through a mouth full of "
                                "food).\n"
                            ),
                            "as_html": (
                                "<p>Cookie Monster is a Muppet on the long "
                                "running children's television show Sesame "
                                "Street. He is best known for his voracious "
                                "appetite and his famous eating phrases: \"Me "
                                "want cookie!\", \"Me eat cookie!\", and \"Om "
                                "nom nom nom\" (said through a mouth full of "
                                "food).</p>\n"
                            ),
                            "raw_text": (
                                "Cookie Monster is a Muppet on the long "
                                "running children's television show Sesame "
                                "Street. He is best known for his voracious "
                                "appetite and his famous eating phrases: \"Me "
                                "want cookie!\", \"Me eat cookie!\", and \"Om "
                                "nom nom nom\" (said through a mouth full of "
                                "food)."
                            ),
                            "as_html_no_tokens": (
                                "<p>Cookie Monster is a Muppet on the long "
                                "running children's television show Sesame "
                                "Street. He is best known for his voracious "
                                "appetite and his famous eating phrases: \"Me "
                                "want cookie!\", \"Me eat cookie!\", and \"Om "
                                "nom nom nom\" (said through a mouth full of "
                                "food).</p>\n"
                            ),
                            "as_markdown": (
                                "Cookie Monster is a Muppet on the long "
                                "running children's television show Sesame "
                                "Street. He is best known for his voracious "
                                "appetite and his famous eating phrases: \"Me "
                                "want cookie!\", \"Me eat cookie!\", and \"Om "
                                "nom nom nom\" (said through a mouth full of "
                                "food)."
                            )
                        }
                    },
                    {
                        "id": "sesame-street-characters-1-3",
                        "title": "Oscar The Grouch",
                        "menu_image": {
                            "square_crop": (
                                "/media/__sized__/content-group/oscar-the-"
                                "grouch-crop-c0-53__0-16-490x490.png"
                            )
                        },
                        "alternate_menu_image": {},
                        "content": {
                            "as_plaintext": (
                                "Oscar the Grouch is a Muppet character on "
                                "the television program Sesame Street. He has "
                                "a green body (during the first season he was "
                                "orange), has no visible nose, and lives "
                                "in a trash can.\n"
                            ),
                            "as_html": (
                                "<p>Oscar the Grouch is a Muppet character on "
                                "the television program Sesame Street. He has "
                                "a green body (during the first season he was "
                                "orange), has no visible nose, and lives "
                                "in a trash can.</p>\n"
                            ),
                            "raw_text": (
                                "Oscar the Grouch is a Muppet character on "
                                "the television program Sesame Street. He has "
                                "a green body (during the first season he was "
                                "orange), has no visible nose, and lives "
                                "in a trash can."
                            ),
                            "as_html_no_tokens": (
                                "<p>Oscar the Grouch is a Muppet character on "
                                "the television program Sesame Street. He has "
                                "a green body (during the first season he was "
                                "orange), has no visible nose, and lives "
                                "in a trash can.</p>\n"
                            ),
                            "as_markdown": (
                                "Oscar the Grouch is a Muppet character on "
                                "the television program Sesame Street. He has "
                                "a green body (during the first season he was "
                                "orange), has no visible nose, and lives "
                                "in a trash can."
                            )
                        }
                    }
                ]
            }
        )
