# -*- coding: utf-8 -*-
#
# Copyright 2012 Jaime Gil de Sagredo Luna
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module is a wrapper on top of the Tornado's HTTPClient."""

import urllib2, base64


class Session(object):
    def __init__(self, domain, auth=None):

        if isinstance(auth, tuple):
            self.base64string = base64.encodestring('%s:%s' % (auth[0], auth[1])).replace('\n', '')
        else:
            self.base64string = None

    def fetch(self, url, method='GET', body=None, **kwargs):
        opener = urllib2.build_opener(urllib2.HTTPSHandler)
        if method == 'PUT' or method == 'POST':
            request = urllib2.Request(url, data=body)
        else:
            request = urllib2.Request(url)
        request.add_header('Content-Type', 'application/json')
        if self.base64string is not None:
            request.add_header("Authorization", "Basic %s" % self.base64string)
        request.get_method = lambda: method
        url = opener.open(request)
        return url

