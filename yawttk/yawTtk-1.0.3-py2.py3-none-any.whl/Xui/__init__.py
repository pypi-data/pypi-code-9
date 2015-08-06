# -*- coding:utf-8 -*-
"""
Copyright® 2013, THOORENS Bruno
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.
* Neither the name of the *xmlTk* nor the names of its contributors may be
used to endorse or promote products derived from this software without specific
prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

from xml.etree import ElementTree as etree

import re, os, sys
if sys.version_info[0] >= 3:
	from urllib import request as urllib2
	from urllib import parse as parse
else:
	import urllib as parse
	import urllib2

urlopen = urllib2.urlopen
urlencode = parse.urlencode

def getXmlDom(url, **param):	
	if os.path.exists(url):
		xmlstring = open(url, "r").read()
	else:
		xmlstring = urlopen(url + (("?" if not url.endswith("?") else "") + urlencode(param)) if len(param) > 0 else "", timeout=2).read().decode()
	xmlstring = re.sub(' xmlns="[^"]+"', '', xmlstring)
	xmlstring = re.sub('<[a-zA-Z]*:', '<', xmlstring)
	xmlstring = re.sub('</[a-zA-Z]*:', '</', xmlstring)
	return etree.fromstring(xmlstring)
