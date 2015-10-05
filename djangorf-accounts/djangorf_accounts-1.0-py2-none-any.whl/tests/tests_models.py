from django.test import TestCase
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
User = get_user_model()

class UserModelTest(TestCase):

    @patch('accounts.signals.create_authentication_token', autospec=True)
    def test_have_an_automatically_generated_token(self, mock_create_token_function):
        post_save.connect(mock_create_token_function, sender=User)
        user = User.objects.create()

        self.assertTrue(mock_create_token_function.called)
        self.assertIsInstance(user._auth_token_cache, Token)

    def test_when_no_username_its_auto_populated(self):
        username = 'Cool name!'

        user_with_no_name = User.objects.create(email='a@b.com', password='Secret!')
        user_with_name = User.objects.create(username=username, email='some@b.com', password='Secret!')

        self.assertEqual(user_with_no_name.username, user_with_no_name.email)
        self.assertEqual(user_with_name.username, username)

    def test_email_cannot_be_empty(self):
        with self.assertRaises(ValidationError):
            user = User(email='', password='Secret!')
            user.full_clean()
            user.save()

    def test_email_is_unique(self):
        email = 'a@b.com'
        with self.assertRaises(IntegrityError):
            User.objects.create(username='Nombre Cool!', email=email, password='Secret!')
            User.objects.create(username='Lame name!', email=email, password='Secret!')

    def test_username_is_unique(self):
        username = 'Nombre Popular!'
        with self.assertRaises(IntegrityError):
            User.objects.create(username=username, email='a@b.com', password='Secret!')
            User.objects.create(username=username, email='otro@b.com', password='Secret!')
