# encoding: utf-8
# Created by Jeremy Bowman on Fri Feb 21 16:06:03 EST 2014
# Copyright (c) 2014, 2015 Safari Books Online. All rights reserved.
#
# This software may be modified and distributed under the terms
# of the 3-clause BSD license.  See the LICENSE file for details.
"""
Yet Another Django Profiler settings tests
"""

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

TEST_PAGE_EXCERPT = 'This is only a test'
HELP_EXCERPT = 'profiling middleware'


class DjangoSettingsTest(TestCase):

    def test_no_profiling(self):
        """Views should work normally when the profiler is not specifically invoked"""
        response = self._get_test_page()
        self.assertContains(response, TEST_PAGE_EXCERPT)

    @override_settings(YADP_ENABLED=True)
    def test_profiler_enabled(self):
        """The profiler should be usable when YADP_ENABLED is True"""
        response = self._get_test_page('profile=help')
        self.assertNotContains(response, TEST_PAGE_EXCERPT)
        self.assertContains(response, HELP_EXCERPT)

    def test_obeys_debug(self):
        """The middleware should be disabled when DEBUG = False and there is no explicit YADP_ENABLED"""
        response = self._get_test_page('profile=help')
        self.assertContains(response, TEST_PAGE_EXCERPT)

    @override_settings(YADP_ENABLED=True, YADP_PROFILE_PARAMETER='other')
    def test_alternate_profile_parameter(self):
        """It should be possible to override the profile parameter name"""
        response = self._get_test_page('profile=help')
        self.assertContains(response, TEST_PAGE_EXCERPT)
        response = self._get_test_page('other=help')
        self.assertContains(response, HELP_EXCERPT)

    def _get_test_page(self, params=''):
        url = reverse('test')
        if params:
            url += '?' + params
        return self.client.get(url)
