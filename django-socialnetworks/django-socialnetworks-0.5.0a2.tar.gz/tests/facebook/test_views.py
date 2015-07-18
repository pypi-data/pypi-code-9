# -*- coding: utf-8 -*-
import httpretty
import json

from urlparse import parse_qs, urlparse, urlunparse

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from sure import expect

from socialnetworks.facebook.clients import FacebookClient
from socialnetworks.facebook.models import FacebookOAuthProfile


class FacebookLoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('socialnetworks:facebook:login')
        self.callback_url = reverse('socialnetworks:facebook:callback')

    def test_view_redirects_to_login_dialog(self):
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
            .should.be.equal(FacebookClient.authorization_url)

        expect(query) \
            .should.be.equal({
                'client_id': ['test-facebook-app'],
                'redirect_uri': ['http://testserver' + self.callback_url],
                'scope': ['email']
            })

    def test_view_sets_default_next_parameter_in_session(self):
        self.client.post('/social/facebook/login/', follow=False)

        expect(self.client.session) \
            .to.have.key('socialnetworks:facebook') \
            .to.have.key('next') \
            .being.equal('/')

    def test_view_sets_next_parameter_in_session(self):
        self.client.post(self.login_url, {'next': '/some-url/'}, follow=False)

        expect(self.client.session) \
            .to.have.key('socialnetworks:facebook') \
            .to.have.key('next') \
            .being.equal('/some-url/')

    def test_view_sets_truthy_only_login_parameter_in_session(self):
        self.client.post(self.login_url, {'only_login': True}, follow=False)

        expect(self.client.session) \
            .to.have.key('socialnetworks:facebook') \
            .to.have.key('only_login') \
            .being.equal('True')

    def test_view_sets_falsy_only_login_parameter_in_session(self):
        self.client.post(self.login_url, {'only_login': False}, follow=False)

        expect(self.client.session) \
            .to.have.key('socialnetworks:facebook') \
            .to.have.key('only_login') \
            .being.equal('False')


class FacebookCallbackTestCase(TestCase):
    def setUp(self):
        httpretty.enable()

        self.client = Client()
        self.callback_url = reverse('socialnetworks:facebook:callback')
        self.setup_url = reverse('socialnetworks:facebook:setup')

    def test_calling_without_verifier_returns_forbidden(self):
        response = self.client.get(self.callback_url)

        expect(response.status_code).should.be.equal(403)

    def test_calling_with_verifier_gets_access_token(self):
        httpretty.register_uri(
            httpretty.POST,
            FacebookClient.access_token_url,
            body=json.dumps({
                'user_id': '123abc',
                'access_token': 'qwertyuiopasdfghjklzxcvbnm',
                'expires': '3600'
            })
        )

        self.client.get(self.callback_url + '?' + 'code=zxcvbnm')

        expect(self.client.session) \
            .to.have.key('socialnetworks:facebook') \
            .to.have.key('service_uid') \
            .to.being.equal('123abc')

        expect(self.client.session) \
            .to.have.key('socialnetworks:facebook') \
            .to.have.key('oauth_access_token') \
            .being.equal('qwertyuiopasdfghjklzxcvbnm')

        expect(self.client.session) \
            .to.have.key('socialnetworks:facebook') \
            .to.have.key('oauth_access_token_secret') \
            .being.none

        expect(self.client.session) \
            .to.have.key('socialnetworks:facebook') \
            .to.have.key('oauth_request_token') \
            .being.none

        expect(self.client.session) \
            .to.have.key('socialnetworks:facebook') \
            .to.have.key('oauth_request_token_secret') \
            .being.none

        expect(self.client.session) \
            .to.have.key('socialnetworks:facebook') \
            .to.have.key('oauth_refresh_token') \
            .being.none

    def test_calling_with_verifier_creates_new_profile(self):
        httpretty.register_uri(
            httpretty.POST,
            FacebookClient.access_token_url,
            body=json.dumps({
                'user_id': '123abc',
                'access_token': 'qwertyuiopasdfghjklzxcvbnm',
                'expires': '3600'
            })
        )

        expect(FacebookOAuthProfile.objects.count()) \
            .should.be.equal(0)

        response = self.client.get(self.callback_url + '?' + 'code=zxcvbnm')

        expect(FacebookOAuthProfile.objects.count()) \
            .should.be.equal(1)

        profile = FacebookOAuthProfile.objects.latest('id')

        expect(profile) \
            .to.have.property('service_uid') \
            .being.equal('123abc')

        expect(profile) \
            .to.have.property('oauth_access_token') \
            .being.equal('qwertyuiopasdfghjklzxcvbnm')

#        expect(self.client.session) \
#            .to.have.key('socialnetworks:facebook') \
#            .to.have.key('service_uid') \
#            .to.being.equal('123abc')
#
#        expect(self.client.session) \
#            .to.have.key('socialnetworks:facebook') \
#            .to.have.key('oauth_access_token') \
#            .being.equal('qwertyuiopasdfghjklzxcvbnm')
#
#        expect(self.client.session) \
#            .to.have.key('socialnetworks:facebook') \
#            .to.have.key('oauth_access_token_secret') \
#            .being.none
#
#        expect(self.client.session) \
#            .to.have.key('socialnetworks:facebook') \
#            .to.have.key('oauth_request_token') \
#            .being.none
#
#        expect(self.client.session) \
#            .to.have.key('socialnetworks:facebook') \
#            .to.have.key('oauth_request_token_secret') \
#            .being.none
#
#        expect(self.client.session) \
#            .to.have.key('socialnetworks:facebook') \
#            .to.have.key('oauth_refresh_token') \
#            .being.none

        expect(self.client.session) \
            .to.have.key('socialnetworks:facebook') \
            .to.have.key('new_user') \
            .being.truthy

        expect(response.status_code) \
            .should.be.equal(302)

        expect(response) \
            .have.key('Location') \
            .being.equal('http://testserver' + self.setup_url)
