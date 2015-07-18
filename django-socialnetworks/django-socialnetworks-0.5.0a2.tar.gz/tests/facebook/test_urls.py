# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test import TestCase

from sure import expect

from socialnetworks.facebook import views


class FacebookUrlsTestCase(TestCase):
    def test_login_url_is_correct(self):
        url = resolve('/social/facebook/login/')

        expect(url) \
            .to.have.property('func') \
            .to.have.property('__name__') \
            .being.equal(views.FacebookDialogRedirectView.__name__)

    def test_callback_url_is_correct(self):
        url = resolve('/social/facebook/callback/')

        expect(url) \
            .to.have.property('func') \
            .to.have.property('__name__') \
            .being.equal(views.FacebookCallbackView.__name__)

    def test_setup_url_is_correct(self):
        url = resolve('/social/facebook/setup/')

        expect(url) \
            .to.have.property('func') \
            .to.have.property('__name__') \
            .being.equal(views.FacebookSetupView.__name__)

    def test_disconnect_url_is_correct(self):
        url = resolve('/social/facebook/disconnect/')

        expect(url) \
            .to.have.property('func') \
            .to.have.property('__name__') \
            .being.equal(views.FacebookOAuthDisconnectView.__name__)
