from django.contrib.auth.models import User
from django.test import TestCase
from .models import Event


class EventsTestCases(TestCase):
    def setUp(self):
        User.objects.create_user('test', 'test@example.com', 'test123')

    def test_todo(self):
        pass
