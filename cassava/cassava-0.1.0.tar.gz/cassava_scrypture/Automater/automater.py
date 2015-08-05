#!/usr/bin/env python
# investigate.py
"""
Check indicators against multiple sites with Automater.
"""




import cassava
import re
from scrypture import webapi
class WebAPI(webapi.WebAPI):
    indicators = webapi.list_input('Domains (Newline Delimited)')
    automater_opt = webapi.radio_field('Automater options',
        choices = [('automater', 'automater (all sources'),
                   ('robtex', 'robtex'),
                   ('fortinet_classify', 'fortinet_classify'),
                   ('vtpDNSIP', 'vtpDNSIP'),
                   ('ipvoid', 'ipvoid'),
                   ('virustotal', 'virustotal'),
                   ('threatexpert', 'threatexpert'),
                   ('vxvault', 'vxvault'),
                   ('unshortme', 'unshortme'),
                   ('urlvoid', 'urlvoid'),
                   ('vtpDNSDom', 'vtpDNSDom'),
                   ('malc0de', 'malc0de'),
                   ('ReputationAuthority', 'ReputationAuthority'),
                   ('FreeGeo', 'FreeGeo'),
                   ('SANS_API', 'SANS_API'),
                   ('totalhash_ip', 'totalhash_ip')],
        default = 'automater')
    submit_button = webapi.submit_button('Submit')

    def run(self, form_input):
        indicators = form_input['indicators']
        automater_opt = form_input['automater_opt']

        if type(indicators) != list:
            indicators = [x.rstrip() for x in re.split('\n', form_input['indicators'])]
            indicators = [x for x in indicators if x != '']

        automater_option_functions = {
            'automater' : cassava.automater.automater,
            'robtex' : cassava.automater.robtex,
            'fortinet_classify' : cassava.automater.fortinet_classify,
            'vtpDNSIP' : cassava.automater.vtpDNSIP,
            'ipvoid' : cassava.automater.ipvoid,
            'virustotal' : cassava.automater.virustotal,
            'threatexpert' : cassava.automater.threatexpert,
            'vxvault' : cassava.automater.vxvault,
            'unshortme' : cassava.automater.unshortme,
            'urlvoid' : cassava.automater.urlvoid,
            'vtpDNSDom' : cassava.automater.vtpDNSDom,
            'malc0de' : cassava.automater.malc0de,
            'ReputationAuthority' : cassava.automater.ReputationAuthority,
            'FreeGeo' : cassava.automater.FreeGeo,
            'SANS_API' : cassava.automater.SANS_API,
            'totalhash_ip' : cassava.automater.totalhash_ip}

        automater_info = []
        for indicator in indicators:
            data = automater_option_functions[automater_opt](indicator)
            automater_info.append(data)

        all_headers = set()
        for a in automater_info:
            for k in a.keys():
                all_headers.update({k})
        all_headers = list(all_headers)

        return {'output_type' : 'table',
                'output' : automater_info,
                'headers' : all_headers}


