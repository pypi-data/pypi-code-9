#!/usr/bin/env python
# whois.py
"""
Whois queries for domains and IPs
"""

import cassava
import re
from scrypture import webapi
class WebAPI(webapi.WebAPI):
    indicators = webapi.list_input('Indicators (Newline Delimited)')
    submit_button = webapi.submit_button('Investigate!')

    def run(self, form_input):
        indicators = form_input['indicators']

        if type(indicators) != list:
            indicators = [x.rstrip() for x in re.split('\n', form_input['indicators'])]
            indicators = [x for x in indicators if x != '']

        whois_info = []
        for indicator in indicators:
            whois_info.append(cassava.whois(indicator))

        headers = []

        return {'output_type' : 'table',
                'output' : whois_info,
                'headers' : whois_info[0].keys()}


