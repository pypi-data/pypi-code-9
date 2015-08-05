#!/usr/bin/env python
# investigate.py
"""
OpenDNS Investigate: find domains registered with a given email address
"""

import cassava
from cassava.opendns import *
from scrypture import webapi
import re

class WebAPI(webapi.WebAPI):
    emails = webapi.list_input('Domains (Newline Delimited)')
    submit_button = webapi.submit_button('Investigate!')

    def run(self, form_input):
        emails = form_input['emails']

        if type(emails) != list:
            emails = [x.decode('utf8', 'ignore').rstrip()
                       for x in re.split('\n', form_input['emails'])]
            emails = [x for x in emails if x != '']

        sgraph_info = []
        for email in emails:
            for ew in email_whois(email)[email]['domains']:
                info = ew
#                info['cooccurrences'] =
                info.update({'indicator' : email})
                sgraph_info.append(info)

        all_headers = set()
        for a in sgraph_info:
            for k in a.keys():
                all_headers.update({k})
        all_headers = list(all_headers)


        return {'output_type' : 'table',
                'output' : sgraph_info,
                'headers' : all_headers}


