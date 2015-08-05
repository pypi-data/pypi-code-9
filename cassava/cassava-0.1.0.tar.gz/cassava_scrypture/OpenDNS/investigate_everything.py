#!/usr/bin/env python
# investigate.py
"""
Scrypture interface for the OpenDNS Investigate API. Allows bulk
lookups of domains and IPs.
"""

import cassava
from cassava.opendns import *
from scrypture import webapi
import re

class WebAPI(webapi.WebAPI):
    domains = webapi.list_input('Domains/IPs (Newline Delimited)')
    verbosity = webapi.radio_field('Verbose?',
                                 choices=[('summary', 'Summarize output'),
                                          ('verbose', 'Full verbose output')],
                                 default='summary')
    submit_button = webapi.submit_button('Investigate!')

    def run(self, form_input):
        domains = form_input['domains']
        verbosity = form_input['verbosity']

        if type(domains) != list:
            domains = [x.decode('utf8', 'ignore').rstrip()
                       for x in re.split('\n', form_input['domains'])]
            domains = [x for x in domains if x != '']

        sgraph_info = []
        for domain in domains:
            sec_info = get_security_info(domain)
            categorization = get_categorization(domain)
            sec_info.update(categorization)
            sec_info.update({'indicator' : domain})
            if cassava.utils.is_ip(domain):
                rr_history_a = rr_history_ip(domain, query_type='A')
                rr_history_ns = rr_history_ip(domain, query_type='NS')
                latest_malicious_domains = get_latest_domains(domain)
                sec_info['link'] = '<a href="https://investigate.opendns.com/ip-view/{}">Investigate</a>'.format(domain)
            else:
                rr_history_a = rr_history_domain(domain, query_type='A')
                rr_history_ns = rr_history_domain(domain, query_type='NS')
                latest_malicious_domains = 'N/A'
                sec_info['link'] = '<a href="https://investigate.opendns.com/domain-view/name/{}/view">Investigate</a>'.format(domain)
                sec_info['whois'] = domain_whois(domain)
                sec_info['whois_entries'] = len(sec_info['whois'])
            sec_info['latest_malicious'] = latest_malicious_domains
            sec_info['past_a_records'] = list(set(rr_history_a))
            sec_info['past_ns_records'] = list(set(rr_history_ns))
            status = {-1 : 'blocked', 0 : 'uncategorized', 1 : 'benign'}
            if 'status' in sec_info and sec_info['status'] in status:
                sec_info['status'] = status[sec_info['status']]
            else:
                sec_info['status'] = 'no entry'

            sgraph_info.append(sec_info)

        all_headers = set()
        for a in sgraph_info:
            for k in a.keys():
                all_headers.update({k})
        all_headers = list(all_headers)

        summary_headers = ['indicator',
                           'link',
                           'status',
                           'securerank2',
                           'content_categories',
                           'threat_type',
                           'security_categories',
                           'past_a_records',
                           'fastflux',
                           'popularity',
                           'past_ns_records ',
                           'latest_malicious',
                           'whois_entries']

        if verbosity == 'verbose':
            headers = all_headers
        else:
            headers = summary_headers


        return {'output_type' : 'table',
                'output' : sgraph_info,
                'headers' : headers}


