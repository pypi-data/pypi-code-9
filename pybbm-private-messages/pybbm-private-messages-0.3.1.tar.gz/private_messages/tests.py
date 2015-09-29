# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import random

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.lorem_ipsum import paragraphs

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from private_messages.models import PrivateMessage, MessageThread, MessageHandler

User = get_user_model()

class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    username = factory.sequence(lambda n: 'test{}'.format(n))
    password = 'test'
    last_name = 'Test'
    email = factory.LazyAttribute(lambda o: '{}@example.com'.format(o.username))

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


class LoremFuzzyAttribute(factory.fuzzy.BaseFuzzyAttribute):

    def __init__(self, max_paras=3, **kwargs):
        super(LoremFuzzyAttribute, self).__init__(**kwargs)
        self.max_paras = max_paras

    def fuzz(self):
        count = random.choice(range(1, self.max_paras + 1))
        return '\n\n'.join(paragraphs(count, common=False))


class ThreadFactory(DjangoModelFactory):
    class Meta:
        model = MessageThread


class PrivateMessageFactory(DjangoModelFactory):

    class Meta:
        model = PrivateMessage

    body = LoremFuzzyAttribute()
    thread = factory.SubFactory(ThreadFactory)

    @factory.post_generation
    def receivers(self, create, receivers, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if receivers:
            for user in receivers:
                MessageHandler.objects.create(message=self, receiver=user)


class PrivateMessageTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(PrivateMessageTests, cls).setUpClass()
        cls.alice = UserFactory.create(username='alice', first_name='Alice')
        cls.bob = UserFactory.create(username='bob', first_name='Bob')
        cls.eve = UserFactory.create(username='eve', first_name='Eve')

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        super(PrivateMessageTests, cls).tearDownClass()

    def test_inbox_view(self):
        response = self.client.get(reverse('private_messages:inbox'))
        self.assertRedirects(response, '{0}?next={1}'.format(reverse('auth_login'), reverse('private_messages:inbox')))
        self.client.login(username='alice', password='test')
        response = self.client.get(reverse('private_messages:inbox'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('private_messages:outbox'))
        self.assertEqual(response.status_code, 200)

        PrivateMessageFactory.create_batch(10, sender=self.bob, receivers=[self.alice])
        response = self.client.get(reverse('private_messages:inbox'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('private_messages:outbox'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        self.client.login(username='bob', password='test')
        response = self.client.get(reverse('private_messages:inbox'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('private_messages:outbox'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_read_message(self):
        message = PrivateMessageFactory.create(sender=self.alice, receivers=[self.bob])
        message_url = reverse('private_messages:read_message', args=[message.pk])

        response = self.client.get(message_url)
        self.assertRedirects(response, '{0}?next={1}'.format(reverse('auth_login'), message_url))
        self.client.login(username='alice', password='test')
        response = self.client.get(message_url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        self.client.login(username='bob', password='test')
        response = self.client.get(message_url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        self.client.login(username='eve', password='test')
        response = self.client.get(message_url)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_send_message(self):
        subject = 'Test Message Sending'
        form_data = {
            'subject': subject,
            'body': LoremFuzzyAttribute().fuzz(),
            'receivers': [self.bob.pk]
        }
        self.client.login(username='alice', password='test')
        response = self.client.post(reverse('private_messages:send_message'), form_data)
        message = PrivateMessage.objects.get(subject=subject, receivers=self.bob, sender=self.alice)
        self.assertRedirects(response, reverse('private_messages:read_message', args=[message.pk]), target_status_code=200)
        self.client.logout()

    def test_strip_sender_from_receivers(self):
        subject = 'Test Strip Sender'
        form_data = {
            'subject': subject,
            'body': LoremFuzzyAttribute().fuzz(),
            'receivers': [self.bob.pk, self.alice.pk]
        }
        self.client.login(username='alice', password='test')
        response = self.client.post(reverse('private_messages:send_message'), form_data)
        message = PrivateMessage.objects.get(subject=subject, receivers=self.bob, sender=self.alice)
        self.assertRedirects(response, reverse('private_messages:read_message', args=[message.pk]), target_status_code=200)
        self.assertNotIn(self.alice, message.receivers.all())

        subject = 'Test Strip Sender 2'
        form_data = {
            'subject': subject,
            'body': LoremFuzzyAttribute().fuzz(),
            'receivers': [self.alice.pk, self.bob.pk, self.alice.pk]
        }
        response = self.client.post(reverse('private_messages:send_message'), form_data)
        message = PrivateMessage.objects.get(subject=subject, receivers=self.bob, sender=self.alice)
        self.assertRedirects(response, reverse('private_messages:read_message', args=[message.pk]), target_status_code=200)
        self.assertNotIn(self.alice, message.receivers.all())
        self.client.logout()
