# -*- coding: utf-8 -*-
'''
Copyright 2011-2015 ramusus
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from datetime import datetime

from django.test import TestCase

from .models import User

USER_ID = '4'
USER_USERNAME = 'zuck'


class FacebookUsersTest(TestCase):

    def test_fetch_user(self):

        self.assertEqual(User.objects.count(), 0)
        User.remote.fetch(USER_ID)
        User.remote.fetch(USER_USERNAME)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.all()[0]

        self.assertEqual(user.graph_id, USER_ID)
        self.assertEqual(user.name, u'Mark Zuckerberg')
        self.assertEqual(user.first_name, 'Mark')
        self.assertEqual(user.last_name, 'Zuckerberg')
        self.assertEqual(user.link, 'https://www.facebook.com/zuck')
        self.assertEqual(user.username, USER_USERNAME)
        self.assertEqual(user.gender, 'male')
        self.assertEqual(user.locale, 'en_US')
        self.assertTrue(isinstance(user.cover, dict))
        self.assertTrue(isinstance(user.updated_time, datetime))
