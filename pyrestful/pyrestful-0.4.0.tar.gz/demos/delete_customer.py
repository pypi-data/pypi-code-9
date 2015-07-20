#!/usr/bin/env python
#
# Copyright 2013 Rodrigo Ancavil del Pino
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# -*- coding: utf-8 -*-

import httplib
import json
import urllib

print 'Delete customer'
print '==============='
id_customer = raw_input('Id Customer      : ')

if len(id_customer) == 0:
	print 'You must indicates id of customer'
else:
	conn = httplib.HTTPConnection("localhost:8080")

	conn.request('DELETE','/customer/%s'%id_customer)

	resp = conn.getresponse()
	data = resp.read()
	if resp.status == 200:
		json_data = json.loads(data)
		print json_data
	else:
		print data