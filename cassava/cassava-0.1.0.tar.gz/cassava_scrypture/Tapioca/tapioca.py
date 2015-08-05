#!/usr/bin/env python
# cassava.py
"""
TAPIOCA Automated Processing for IOC Analysis
"""

import cassava
from cassava.opendns import *
from scrypture import webapi
import re

class WebAPI(webapi.WebAPI):
    domains = webapi.list_input('Domains and IPs (Newline Delimited)')
    verbosity = webapi.radio_field('Verbose?',
                                 choices=[('summary', 'Summarize output'),
                                          ('verbose', 'Full verbose output')],
                                 default='summary')
    submit_button = webapi.submit_button('Look it all up!')

    def run(self, form_input):
        domains = form_input['domains']
        verbosity = form_input['verbosity']

        if type(domains) != list:
            domains = [x.decode('utf8', 'ignore').rstrip()
                       for x in re.split('\n', form_input['domains'])]
            domains = [x for x in domains if x != '']

        all_info = []

        for domain in domains:
            sec_info = {'indicator' : domain}
            ### OpenDNS ###
            try:
                sec_info.update(get_security_info(domain))
                categorization = get_categorization(domain)
                sec_info.update(categorization)
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
            except:
                print "OpenDNS problems. Valid API key?"

            ### Automater ###
            sec_info.update(cassava.automater.automater(domain))

            ### VirusTotal ###
            try:
                if cassava.utils.is_ip(domain):
                    sec_info.update(cassava.virustotal.get_ip_report(domain)[0])
                else:
                    sec_info.update(cassava.virustotal.get_domain_report(domain)[0])
                sec_info['vtlink'] = '<a href="{}">VirusTotal</a>'.format(sec_info['permalink'])
            except:
                print "VirusTotal problems. Valid API key?"

            all_info.append(sec_info)


        all_headers = set()
        for a in all_info:
            for k in a.keys():
                all_headers.update({k})
        all_headers = list(all_headers)

        summary_headers = ['indicator',
                           'positives',
                           'total',
                           'status',
                           'securerank2',
                           'content_categories',
                           'threat_type',
                           'security_categories',
                           'fastflux',
                           'popularity',
                           'latest_malicious',
                           'link',
                           'vtlink',
                           'BitDefender category',
                           'Websense ThreatSeeker category',
                           'Webutation domain info',
                           'whois_entries',
                           'TrendMicro category',
                           'categories'
                           'mc_date',
                           'uv_domain',
                           'mc_ip',
                           'uv_location',
                           'vt_pdnsurl',
                           'un_redirect',
                           'uv_country',
                           'mc_country',
                           'vt_pdnsip',
                           'mc_asn',
                           'uv_blacklists',
                           'uv_ip',
                           'mc_md5',
                           'mc_asn_name',
                           'fnet_url',]

        if verbosity == 'verbose':
            headers = all_headers
        else:
            headers = summary_headers

        return {'output_type' : 'table',
                'output' : all_info,
                'headers' : headers}


