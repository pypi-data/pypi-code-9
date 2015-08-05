"""
VirusTotal file lookup (by SHA256)
"""

import cassava

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    domains = webapi.list_input('Domains and IPs (Newline Delimited)')
    submit_button = webapi.submit_button('Totally!')

    def run(self, form_input):
        domains = form_input['domains']

        if type(domains) != list:
            domains = [x.rstrip() for x in re.split('\n', form_input['domains'])]
            domains = [x for x in domains if x != '']

        vt_reports = cassava.virustotal.get_vt_file_lookup(domains)

        headers = ['scan_id ',
                   'positives',
                   'total',
                   'scans',
                   'sha256',
                   'sha1',
                   'md5',
                   'resource',
                   'response_code',
                   'scan_date',
                   'permalink',
                   'verbose_msg']

        return {'output_type' : 'table',
                'output' : vt_reports,
                'headers' : headers}
