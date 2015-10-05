from django.test import TestCase
from rest_framework.test import APIClient

from django.core.urlresolvers import reverse
from rest_framework import status
from accounts.serializers import UNAUTHORIZED_MESSAGE
from accounts.views import BAD_REQUEST_SIGNUP
from django.conf import settings

from rest_framework.authtoken.models import Token

import json
import pytz
import datetime

from django.contrib.auth import get_user_model
User = get_user_model()

class SignupViewTests(TestCase):

    def test_can_create_new_user_with_email(self):
        email = 'a@b.com'

        self.client.post(
            reverse('signup'),
            data={
                'email': email,
                'password': 'Secret!'
            }
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, email)

    def test_cannot_create_duplicated_user(self):
        email = "a@b.com"
        password = "secret!"
        User.objects.create_user(username='Cool name!', email=email, password=password)

        response = self.client.post(
            reverse('signup'),
            data={
                "email": email,
                "password": password
            }
        )

        self.assertEquals(BAD_REQUEST_SIGNUP, json.loads(response.content.decode())['error'])

    def test_on_success_return_token(self):
        email = 'a@b.com'
        password = "Secret!"

        response = self.client.post(
            reverse('signup'),
            data={
                "email": email,
                "password": password
            }
        )

        user = User.objects.first()
        token, _ = Token.objects.get_or_create(user=user)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(json.loads(response.content.decode())['token'], token.key)

class LoginViewTests(TestCase):

    def test_can_login_with_user_name(self):
        username = 'a@b.com'
        password = 'secret!'
        valid_user = User.objects.create_user(username=username, password=password)

        response = self.client.post(
            reverse('login'),
            data={
                "username": username,
                "password": password
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], str(valid_user._auth_token_cache))

    def test_can_login_with_email(self):
        email = 'a@b.com'
        password = 'secret!'
        valid_user = User.objects.create_user(username='a', email=email, password=password)

        response = self.client.post(
            reverse('login'),
            data={
                'email': email,
                'password': password
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], str(valid_user._auth_token_cache))

    def test_return_error_when_try_to_login_with_wrong_credentials(self):
        response = self.client.post(
            reverse('login'),
            data={
                'username': 'Wrong user!',
                'password': 'Bad password'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(UNAUTHORIZED_MESSAGE, response.content.decode())

    def test_token_is_renew_when_expired(self):
        email = 'a@b.com'
        password = 'secret!'

        user = User.objects.create_user(username='Cool name!', email=email, password=password)
        user._auth_token_cache.created = user._auth_token_cache.created - datetime.timedelta(hours=settings.EXPIRATION_TIME)
        user._auth_token_cache.save()

        expired_token = user._auth_token_cache.key

        response = self.client.post(
            reverse('login'),
            data={
                'email': email,
                'password': password
            }
        )

        new_token = Token.objects.get(user=user)
        self.assertNotEqual(expired_token, new_token.key)

class LogoutViewTests(TestCase):

    def test_can_login_with_user_name(self):
        user = User.objects.create_user(username='Cool Name!', email='a@b.com', password='secret!')
        token = user._auth_token_cache
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = client.post(
            reverse('logout'),
        )
        title = 'My first recipe!'
        body = 'Example text for my fisrt recipe.'

        self.assertEqual(Token.objects.all().count(), 0)
        self.assertEqual(User.objects.all().count(), 1)
