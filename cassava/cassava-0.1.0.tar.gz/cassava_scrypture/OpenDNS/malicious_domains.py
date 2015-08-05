#!/usr/bin/env python
# malicious_domains.py
"""
OpenDNS Investigate latest malicious domains for an IP
"""

import cassava
from cassava.opendns import *
from scrypture import webapi
import re

class WebAPI(webapi.WebAPI):
    domains = webapi.list_input('IPs (Newline Delimited)')
    submit_button = webapi.submit_button('Investigate!')

    def run(self, form_input):
        domains = form_input['domains']

        if type(domains) != list:
            domains = [x.decode('utf8', 'ignore').rstrip()
                       for x in re.split('\n', form_input['domains'])]
            domains = [x for x in domains if x != '']

        sgraph_info = []
        for domain in domains:
            info = {}
            info['malicious_domains'] = get_latest_malicious_domains(domain)
            info.update({'indicator' : domain})
            sgraph_info.append(info)

        all_headers = set()
        for a in sgraph_info:
            for k in a.keys():
                all_headers.update({k})
        all_headers = list(all_headers)


        return {'output_type' : 'table',
                'output' : sgraph_info,
                'headers' : all_headers}


