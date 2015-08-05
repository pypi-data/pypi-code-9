"""
VirusTotal domain lookup
"""

import cassava
import re

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    domains = webapi.list_input('Domains and IPs (Newline Delimited)')
    submit_button = webapi.submit_button('Totally!')

    def run(self, form_input):
        domains = form_input['domains']

        if type(domains) != list:
            domains = [x.rstrip() for x in re.split('\n', form_input['domains'])]
            domains = [x for x in domains if x != '']

        print '========>'
        print domains
        vt_reports = cassava.virustotal.get_domain_report(domains)
        reports_out = []
        print vt_reports
        for info in vt_reports:
            info['vtlink'] = '<a href="{}">VirusTotal</a>'.format(info['permalink'])
            reports_out.append(info)

        headers = ['indicator',
                   'positives',
                   'total',
                   'scans',
                   'scan_date',
                   'permalink',
                   'BitDefender category',
                   'domain_siblings',
                   'undetected_referrer_samples',
                   'whois',
                   'whois_timestamp',
                   'WOT domain info',
                   'Websense ThreatSeeker category',
                   'Webutation domain info',
                   'subdomains',
                   'resolutions',
                   'detected_communicating_samples',
                   'TrendMicro category',
                   'categories']

        return {'output_type' : 'table',
                'output' : reports_out,
                'headers' : headers}
