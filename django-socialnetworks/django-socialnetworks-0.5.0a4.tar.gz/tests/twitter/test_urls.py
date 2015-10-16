# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test import TestCase

from sure import expect

from socialnetworks.twitter import views


class TwitterUrlsTestCase(TestCase):
    def test_login_url_is_correct(self):
        url = resolve('/social/twitter/login/')

        expect(url) \
            .to.have.property('func') \
            .to.have.property('__name__') \
            .being.equal(views.TwitterDialogRedirectView.__name__)

    def test_callback_url_is_correct(self):
        url = resolve('/social/twitter/callback/')

        expect(url) \
            .to.have.property('func') \
            .to.have.property('__name__') \
            .being.equal(views.TwitterCallbackView.__name__)

    def test_setup_url_is_correct(self):
        url = resolve('/social/twitter/setup/')

        expect(url) \
            .to.have.property('func') \
            .to.have.property('__name__') \
            .being.equal(views.TwitterSetupView.__name__)

    def test_disconnect_url_is_correct(self):
        url = resolve('/social/twitter/disconnect/')

        expect(url) \
            .to.have.property('func') \
            .to.have.property('__name__') \
            .being.equal(views.TwitterOAuthDisconnectView.__name__)
