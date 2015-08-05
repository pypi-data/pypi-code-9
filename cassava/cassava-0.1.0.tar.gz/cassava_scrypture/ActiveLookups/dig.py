#!/usr/bin/env python
# investigate.py
"""
Dig domains using system dig command.
System dependent: Unixy systems only, must have dig installed.
"""

import cassava
import re
from scrypture import webapi
class WebAPI(webapi.WebAPI):
    domains = webapi.list_input('Domains (Newline Delimited)')
    submit_button = webapi.submit_button('Dig')

    def run(self, form_input):
        domains = form_input['domains']

        if type(domains) != list:
            domains = [x.rstrip() for x in re.split('\n', form_input['domains'])]
            domains = [x for x in domains if x != '']

        dig_info = []
        for domain in domains:
            dig_info.append(cassava.dig(domain))

        return {'output_type' : 'table',
                'output' : dig_info,
                'headers' : dig_info[0].keys()}


