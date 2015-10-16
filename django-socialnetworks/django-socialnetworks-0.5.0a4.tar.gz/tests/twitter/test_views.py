# -*- coding: utf-8 -*-
import httpretty
import json

from urlparse import parse_qs, urlparse, urlunparse

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from sure import expect

from socialnetworks.twitter.clients import TwitterClient
from socialnetworks.twitter.models import TwitterOAuthProfile


class TwitterLoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('socialnetworks:twitter:login')
        self.callback_url = reverse('socialnetworks:twitter:callback')

    def register_normal_flow(self):
        httpretty.enable()
        httpretty.register_uri(
            httpretty.POST,
            TwitterClient.request_token_url,
            body=json.dumps({
                'oauth_token': 'TestTwitterOAuthRequestToken',
                'oauth_token_secret': 'TestTwitterOAuthRequestTokenSecret',
                'oauth_callback_confirmed': True
            })
        )

    def test_view_redirects_to_login_dialog(self):
        self.register_normal_flow()
        response = self.client.post(self.login_url, follow=False)

        expect(response.status_code) \
            .should.be.equal(302)

        expect(response) \
            .have.key('Location')

        parsed = urlparse(response['Location'])
        query = parse_qs(parsed.query)
        url = urlunparse((
            parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

        expect(url) \
            .should.be.equal(TwitterClient.authorization_url)

        expect(query) \
            .should.be.equal({
                'oauth_token': ['TestTwitterOAuthRequestToken'],
            })

    def test_view_sets_oauth_parameters_in_session(self):
        self.register_normal_flow()
        self.client.post(self.login_url, follow=False)

        expect(self.client.session) \
            .to.have.key('socialnetworks:twitter') \
            .to.have.key('oauth_request_token') \
            .being.equal('TestTwitterOAuthRequestToken')

        expect(self.client.session) \
            .to.have.key('socialnetworks:twitter') \
            .to.have.key('oauth_request_token_secret') \
            .being.equal('TestTwitterOAuthRequestTokenSecret')

    def test_view_sets_default_next_parameter_in_session(self):
        self.register_normal_flow()
        self.client.post('/social/twitter/login/', follow=False)

        expect(self.client.session) \
            .to.have.key('socialnetworks:twitter') \
            .to.have.key('next') \
            .being.equal('/')

    def test_view_sets_next_parameter_in_session(self):
        self.register_normal_flow()
        self.client.post(self.login_url, {'next': '/some-url/'}, follow=False)

        expect(self.client.session) \
            .to.have.key('socialnetworks:twitter') \
            .to.have.key('next') \
            .being.equal('/some-url/')

    def test_view_sets_truthy_only_login_parameter_in_session(self):
        self.register_normal_flow()
        self.client.post(self.login_url, {'only_login': True}, follow=False)

        expect(self.client.session) \
            .to.have.key('socialnetworks:twitter') \
            .to.have.key('only_login') \
            .being.equal('True')

    def test_view_sets_falsy_only_login_parameter_in_session(self):
        self.register_normal_flow()
        self.client.post(self.login_url, {'only_login': False}, follow=False)

        expect(self.client.session) \
            .to.have.key('socialnetworks:twitter') \
            .to.have.key('only_login') \
            .being.equal('False')


class TwitterCallbackTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('socialnetworks:twitter:login')
        self.callback_url = reverse('socialnetworks:twitter:callback')
        self.setup_url = reverse('socialnetworks:twitter:setup')

    def register_normal_flow(self):
        httpretty.enable()
        httpretty.register_uri(
            httpretty.POST,
            TwitterClient.request_token_url,
            body=json.dumps({
                'oauth_token': 'TestTwitterOAuthRequestToken',
                'oauth_token_secret': 'TestTwitterOAuthRequestTokenSecret',
                'oauth_callback_confirmed': True
            })
        )
        httpretty.register_uri(
            httpretty.POST,
            TwitterClient.access_token_url,
            body=json.dumps({
                'oauth_token': 'TestTwitterOAuthAccessToken',
                'oauth_token_secret': 'TestTwitterOAuthAccessTokenSecret',
            })
        )
        httpretty.register_uri(
            httpretty.GET,
            TwitterClient.token_debug_url,
            body=json.dumps({
                'id': 123456,
                'name': 'Test User',
                'screen_name': 'TestUserOfficial',
            })
        )

    def test_calling_without_verifier_returns_forbidden(self):
        response = self.client.get(self.callback_url)

        expect(response.status_code) \
            .should.be.equal(403)

    def test_calling_with_verifier_gets_access_token(self):
        callback_url = '{0}?oauth_token={1}&oauth_verifier={2}'

        self.register_normal_flow()
        self.client.post(self.login_url, follow=False)
        self.client.get(callback_url.format(
            self.callback_url,
            'TestTwitterOAuthRequestToken',
            'TestTwitterOAuthVerifier'
        ))

        expect(self.client.session) \
            .to.have.key('socialnetworks:twitter') \
            .to.have.key('service_uid') \
            .to.being.equal('123456')

        expect(self.client.session) \
            .to.have.key('socialnetworks:twitter') \
            .to.have.key('oauth_access_token') \
            .being.equal('TestTwitterOAuthAccessToken')

        expect(self.client.session) \
            .to.have.key('socialnetworks:twitter') \
            .to.have.key('oauth_access_token_secret') \
            .being.equal('TestTwitterOAuthAccessTokenSecret')

        expect(self.client.session) \
            .to.have.key('socialnetworks:twitter') \
            .to.have.key('oauth_request_token') \
            .being.equal('TestTwitterOAuthRequestToken')

        expect(self.client.session) \
            .to.have.key('socialnetworks:twitter') \
            .to.have.key('oauth_request_token_secret') \
            .being.equal('TestTwitterOAuthRequestTokenSecret')

        expect(self.client.session) \
            .to.have.key('socialnetworks:twitter') \
            .to.have.key('oauth_refresh_token') \
            .being.none

    def test_calling_with_verifier_creates_new_profile(self):
        callback_url = '{0}?oauth_token={1}&oauth_verifier={2}'

        expect(TwitterOAuthProfile.objects.count()) \
            .should.be.equal(0)

        self.register_normal_flow()
        self.client.post(self.login_url, follow=False)

        response = self.client.get(callback_url.format(
            self.callback_url,
            'TestTwitterOAuthRequestToken',
            'TestTwitterOAuthVerifier'
        ))

        expect(TwitterOAuthProfile.objects.count()) \
            .should.be.equal(1)

        profile = TwitterOAuthProfile.objects.latest('id')

        expect(profile) \
            .to.have.property('user') \
            .being.none

        expect(profile) \
            .to.have.property('service_uid') \
            .being.equal('123456')

        expect(profile) \
            .to.have.property('oauth_access_token') \
            .being.equal('TestTwitterOAuthAccessToken')

        expect(profile) \
            .to.have.property('oauth_access_token_secret') \
            .being.equal('TestTwitterOAuthAccessTokenSecret')

        expect(profile) \
            .to.have.property('oauth_request_token') \
            .being.equal('TestTwitterOAuthRequestToken')

        expect(profile) \
            .to.have.property('oauth_request_token_secret') \
            .being.equal('TestTwitterOAuthRequestTokenSecret')

        expect(response.status_code) \
            .should.be.equal(302)

        expect(response) \
            .have.key('Location') \
            .being.equal('http://testserver' + self.setup_url)
