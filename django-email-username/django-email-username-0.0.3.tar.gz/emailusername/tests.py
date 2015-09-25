from django.contrib.auth import authenticate
from django.test import TestCase
from emailusername.models import User


class UserTests(TestCase):

    def test_authenticate(self):
        u1 = User.objects.create_user(email='foobar@example.com', password='pass')
        u2 = authenticate(email='foobar@example.com', password='pass')
        self.assertEqual(u1, u2)
