__author__ = 'phg49389'

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# fetch_array requires a username as the first part of the url, and an optional filepath as the second.
# fetch/<username> or fetch/<username>/<path: called> in Flask terms
from fetcher import fetch_array

# Because Django does first url match returning, I'm putting the longer match first.
# The first url listens for subsequent fetches, which go to subfolders.
# The second url listens for the first fetch, which gets the top-level structure by default.
# Django should call fetch_array($, $) for the first url, and fetch_array($) for the second.


def print_calls(args):
    print args

urlpatterns = patterns('sample1',
                       url(r'^fetch/(.*)/(.*)$', fetch_array),
                       url(r'^fetch/(.*)$', print_calls),
                       )
urlpatterns += staticfiles_urlpatterns()
