from django.test import TestCase

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
User = get_user_model()

class AuthenticationTest(TestCase):

    def test_can_authenticate_with_username(self):
        username = 'a@b.com'
        password = 'secret!'
        User.objects.create_user(username=username, password=password)
        user = authenticate(username=username, password=password)
        self.assertIsNotNone(user)

    def test_can_authenticate_with_email(self):
        email = 'a@b.com'
        password = 'secret!'
        User.objects.create_user(username='Cool name!', email=email, password=password)
        user = authenticate(email=email, password=password)
        self.assertIsNotNone(user)
