"""
VirusTotal IP lookup
"""

import cassava
import re

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    indicators = webapi.list_input('IPs (Newline Delimited)')
    submit_button = webapi.submit_button('Totally!')

    def run(self, form_input):
        indicators = form_input['indicators']

        if type(indicators) != list:
            indicators = [x.rstrip() for x in re.split('\n', form_input['indicators'])]
            indicators = [x for x in indicators if x != '']

        vt_reports = cassava.virustotal.get_ip_report(indicators)
        reports_out = []
        for info in vt_reports:
            if 'permalink' in info:
                info['vtlink'] = '<a href="{}">VirusTotal</a>'.format(info['permalink'])
            reports_out.append(info)

        headers = ['indicator',
                   'positives',
                   'total',
                   'scans',
                   'scan_date',
                   'permalink',
                   'detected_referrer_samples',
                   'undetected_referrer_samples',
                   'detected_downloaded_samples',
                   'undetected_downloaded_samples',
                   'detected_communicating_samples',
                   'undetected_communicating_samples',
                   'response_code',
                   'as_owner',
                   'verbose_msg',
                   'detected_urls',
                   'country',
                   'resolutions',
                   'asn']

        return {'output_type' : 'table',
                'output' : reports_out,
                'headers' : headers}
