import datetime
import logging
from django.test import TestCase, Client, override_settings
from django.test.utils import patch_logger
from blacklist import models


class BlacklistingDecoratorTestCase(TestCase):
    user_agent_ff = 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.0.1'
    user_agent_re = '.*Gecko.*'
    user_agent_not_matched_re = '.*Windows.*'

    ip = '176.34.155.20'

    def setUp(self):
        # Every test needs a client.
        self.client = Client(HTTP_USER_AGENT=self.user_agent_ff,
                             REMOTE_ADDR=self.ip)

    def test_request_log(self):
        # Check that there is no request logs
        self.assertFalse(bool(models.RequestLog.objects.all()))

        # Issue a not logged request.
        response = self.client.get('/demo/no_log/')
        self.assertEqual(response.status_code, 200)
        # Check that there is still no request logs
        self.assertFalse(bool(models.RequestLog.objects.all()))

        # Issue logged request.
        response = self.client.get('/demo/log_no_name/')
        self.assertEqual(response.status_code, 200)
        # Check that request log have been created
        self.assertEqual(models.RequestLog.objects.count(), 1)
        request_log = models.RequestLog.objects.all()[0]
        self.assertEqual(request_log.ip, self.ip)
        self.assertEqual(request_log.user_agent, self.user_agent_ff)
        self.assertEqual(request_log.path, '/demo/log_no_name/')
        self.assertIsNone(request_log.view)
        self.assertEqual(request_log.method, 'GET')
        request_log.delete()

        # Issue logged request with view name
        response = self.client.get('/demo/log/')
        self.assertEqual(response.status_code, 200)
        request_log = models.RequestLog.objects.all()[0]
        self.assertEqual(request_log.path, '/demo/log/')
        self.assertEqual(request_log.view, 'log')
        request_log.delete()

        # issue a logged request with view name and namespace
        response = self.client.get('/ns_demo/log/')
        self.assertEqual(response.status_code, 200)
        # Check that request log have been created
        request_log = models.RequestLog.objects.all()[0]
        self.assertEqual(request_log.path, '/ns_demo/log/')
        self.assertEqual(request_log.view, 'demo:log')
        request_log.delete()

    def test_block_rules(self):
        # Check that there is no blocking rules
        self.assertFalse(bool(models.BlockRules.objects.all()))

        # Request would not be blocked when there is no blocking rules.
        response = self.client.get('/demo/no_log/')
        self.assertEqual(response.status_code, 200)

        # Block by ip
        rule = models.BlockRules.objects.create(ip=self.ip, enabled=True)
        with patch_logger('django.request', 'warning') as log_messages:
            response = self.client.get('/demo/no_log/')
            self.assertEqual(response.status_code, 403)
            self.assertEqual(log_messages, ['Forbidden (Block rule #{0}): /demo/no_log/'.format(rule.id),
                                            'Forbidden (Permission denied): /demo/no_log/'])
        rule.delete()

        # Block by user_agent regexp
        rule = models.BlockRules.objects.create(user_agent=self.user_agent_re, enabled=True)
        response = self.client.get('/demo/no_log/')
        self.assertEqual(response.status_code, 403)
        rule.delete()

        rule = models.BlockRules.objects.create(user_agent=self.user_agent_not_matched_re, enabled=True)
        response = self.client.get('/demo/no_log/')
        self.assertEqual(response.status_code, 200)
        rule.delete()

        # Block specific path
        rule = models.BlockRules.objects.create(ip=self.ip, path='/demo/no_log/', enabled=True)
        response = self.client.get('/demo/no_log/')
        self.assertEqual(response.status_code, 403)
        response = self.client.get('/demo/log/')
        self.assertEqual(response.status_code, 200)
        rule.delete()

        # Block path regexp
        rule = models.BlockRules.objects.create(ip=self.ip, path='.*log.*', enabled=True)
        response = self.client.get('/demo/no_log/')
        self.assertEqual(response.status_code, 403)
        response = self.client.get('/demo/log/')
        self.assertEqual(response.status_code, 403)
        rule.delete()

        # Block specific view name
        rule = models.BlockRules.objects.create(ip=self.ip, view='no_log', enabled=True)
        response = self.client.get('/demo/no_log/')
        self.assertEqual(response.status_code, 403)
        response = self.client.get('/demo/log/')
        self.assertEqual(response.status_code, 200)
        rule.delete()

        # check PERMISSION_DENIED_CALLBACK setting
        rule = models.BlockRules.objects.create(ip=self.ip, enabled=True)
        class InCallbackException(Exception): pass
        def permission_denied_callback(callback_rule, request):
            self.assertEqual(rule.pk, callback_rule.pk)
            self.assertEqual(request.META['REMOTE_ADDR'], self.ip)
            raise InCallbackException
        models.permission_denied_callback, permission_denied_callback_backup = permission_denied_callback, models.permission_denied_callback
        with self.assertRaises(InCallbackException):
            self.client.get('/demo/no_log/')
        rule.delete()
        models.permission_denied_callback = permission_denied_callback_backup

    # @override_settings(REMOTE_IP_HEADER='X_REAL_IP') -- doesn't work with custom settings
    def test_ip_header_settings(self):
        models._ip_header = 'X_REAL_IP'

        self.assertFalse(bool(models.RequestLog.objects.count()))

        # Check Request Log functionality
        response = self.client.get('/demo/log/')
        self.assertEqual(response.status_code, 200)
        request_log = models.RequestLog.objects.all()[0]
        self.assertEqual(request_log.path, '/demo/log/')
        self.assertIsNone(request_log.ip)
        request_log.delete()

        client = Client(HTTP_USER_AGENT=self.user_agent_ff,
                        X_REAL_IP=self.ip)
        response = client.get('/demo/log/')
        self.assertEqual(response.status_code, 200)
        request_log = models.RequestLog.objects.all()[0]
        self.assertEqual(request_log.path, '/demo/log/')
        self.assertEqual(request_log.ip, self.ip)
        request_log.delete()

        # Check Block Rules functionality
        # Block by ip
        rule = models.BlockRules.objects.create(ip=self.ip, enabled=True)
        response = self.client.get('/demo/no_log/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/demo/no_log/')
        self.assertEqual(response.status_code, 403)
        rule.delete()

        # check callable REMOTE_IP_HEADER setting
        fake_ip = '254.0.0.254'
        models._ip_header = lambda x: fake_ip if x.get('X_REAL_IP') == 'fake' else x.get('X_REAL_IP')
        client = Client(HTTP_USER_AGENT=self.user_agent_ff,
                        X_REAL_IP=self.ip)
        response = client.get('/demo/log/')
        self.assertEqual(response.status_code, 200)
        request_log = models.RequestLog.objects.all()[0]
        self.assertEqual(request_log.path, '/demo/log/')
        self.assertEqual(request_log.ip, self.ip)
        request_log.delete()
        client = Client(HTTP_USER_AGENT=self.user_agent_ff,
                        X_REAL_IP='fake')
        response = client.get('/demo/log/')
        self.assertEqual(response.status_code, 200)
        request_log = models.RequestLog.objects.all()[0]
        self.assertEqual(request_log.path, '/demo/log/')
        self.assertEqual(request_log.ip, fake_ip)
        request_log.delete()

        models._ip_header = 'REMOTE_ADDR'


class RequestLogManagerTestCase(TestCase):
    user_agent_ch = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36'
    ip = '46.51.197.89'

    def setUp(self):
        self.client = Client(HTTP_USER_AGENT=self.user_agent_ch,
                             REMOTE_ADDR=self.ip)

    def test_create_blocking_rules(self):
        if not models._auto_blocking_rules:
            models._auto_blocking_rules = ({},)
        # 1. Basic blocking
        self.assertFalse(bool(models.BlockRules.objects.all()))
        models._auto_blocking_rules[0].update({
            'RULE': {
                'ip': '.*',
            },
            'PERIOD': datetime.timedelta(days=1),
            'BLOCK_AFTER': 10,
            'ENABLED': True,
            'PROPOSAL': False,
            'NOTIFY': ()
        })
        [self.client.get('/demo/log/') for x in range(10)]

        self.assertFalse(bool(models.BlockRules.objects.all()))
        models.RequestLog.objects.create_blocking_rules()
        self.assertEqual(models.BlockRules.objects.count(), 1)
        rule = models.BlockRules.objects.all()[0]
        self.assertEqual(rule.ip, self.ip)
        self.assertIsNone(rule.user_agent)
        self.assertIsNone(rule.method)
        self.assertIsNone(rule.path)
        self.assertIsNone(rule.view)
        self.assertTrue(rule.enabled)
        rule.delete()

        # 2. Disabled rule doesn't do anything
        models._auto_blocking_rules[0].update({'ENABLED': False})
        self.assertFalse(bool(models.BlockRules.objects.all()))
        models.RequestLog.objects.create_blocking_rules()
        self.assertFalse(bool(models.BlockRules.objects.all()))
        models._auto_blocking_rules[0].update({'ENABLED': True})

        # 3. Proposal means that rule will be created but not applied
        models._auto_blocking_rules[0].update({'PROPOSAL': True})
        self.assertFalse(bool(models.BlockRules.objects.all()))
        models.RequestLog.objects.create_blocking_rules()
        self.assertEqual(models.BlockRules.objects.count(), 1)
        rule = models.BlockRules.objects.all()[0]
        self.assertFalse(rule.enabled)
        models._auto_blocking_rules[0].update({'PROPOSAL': False})
        rule.delete()

        # 4. Notification method executed when NONIFY setting is presented
        models._auto_blocking_rules[0].update({'NOTIFY': (
            ('Mikhail Nacharov', 'mnach@ya.ru'),
        )})

        class NotifyExecuted(Exception): pass

        def fake_notify(*args, **kwargs):
            raise NotifyExecuted

        backup, models.RequestLog.objects._notify_users = \
            models.RequestLog.objects._notify_users, fake_notify
        self.assertFalse(bool(models.BlockRules.objects.all()))
        self.assertRaises(NotifyExecuted, models.RequestLog.objects.create_blocking_rules)
        self.assertEqual(models.BlockRules.objects.count(), 1)
        models.BlockRules.objects.all()[0].delete()
        models.RequestLog.objects._notify_users = backup
        models._auto_blocking_rules[0].update({'NOTIFY': ()})

        # 5. Create block rule for specific view
        models._auto_blocking_rules[0].update({'RULE': {
            'ip': '.*',
            'view': '.*log.*'
        },})
        self.assertFalse(bool(models.BlockRules.objects.all()))
        models.RequestLog.objects.create_blocking_rules()
        self.assertEqual(models.BlockRules.objects.count(), 1)
        rule = models.BlockRules.objects.all()[0]
        self.assertEqual(rule.ip, self.ip)
        self.assertEqual(rule.view, 'log')
        rule.delete()

        # 6. Create block rule for group of agents per agent
        models._auto_blocking_rules[0].update({'RULE': {
            'ip': '.*',
            'user_agent': '.*Chrome.*',
        },})
        self.assertFalse(bool(models.BlockRules.objects.all()))
        models.RequestLog.objects.create_blocking_rules()
        self.assertEqual(models.BlockRules.objects.count(), 1)
        rule = models.BlockRules.objects.all()[0]
        self.assertEqual(rule.ip, self.ip)
        self.assertEqual(rule.user_agent, self.user_agent_ch)
        rule.delete()

        # 7. Create block rule for group of agents at once
        models._auto_blocking_rules[0].update({'RULE': {
            'ip': '.*',
            'user_agent': '.*Chrome.*',
            'user_agent_re': True,
        },})
        self.assertFalse(bool(models.BlockRules.objects.all()))
        models.RequestLog.objects.create_blocking_rules()
        self.assertEqual(models.BlockRules.objects.count(), 1)
        rule = models.BlockRules.objects.all()[0]
        self.assertEqual(rule.ip, self.ip)
        self.assertEqual(rule.user_agent, '.*Chrome.*')
        rule.delete()

    def test_user_notification(self):
        class SendmailExecuted(Exception): pass

        def fake_send_mail(*args, **kwargs):
            raise SendmailExecuted

        backup, models.send_mail = \
            models.send_mail, fake_send_mail

        self.assertRaises(SendmailExecuted, models.RequestLog.objects._notify_users, (), dict(), True, ('root@localhost',))

        models.send_mail = backup

logging.basicConfig(level=logging.INFO)
