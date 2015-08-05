import config

'''
TAPIOCA

Python package with tons of utilities
Exposes simple, easy to use/understand data without needing to deal with details of the API response / fancy JSON parsing
Database 'cache' layer is optional


Tapioca Automated Processing for IOC Analysis
Tapioca takes a bunch of IOCs (IPs or domain names right now) and does a bunch of analysis.
'''

class Tapioca(object):
    def __init__(self):
        self.inv = investigate_wrapper.InvestigateWrapper(config.OpenDNS_APIKEY)

        self.scrypture = scrypture_api.ScryptureAPI(
                         username=config.LDAP_USERNAME,
                         password=config.LDAP_PASSWORD)

        self.splunk_service = splunklib.client.connect(
                              host=config.SPLUNK_HOST,
                              port=config.SPLUNK_PORT,
                              username=config.LDAP_USERNAME,
                              password=config.LDAP_PASSWORD,
                              scheme=config.SPLUNK_SCHEME)

        self.splunk_flow_fields = ['dest_ip',
                                   'dest_port',
                                   'src_ip',
                                   'src_port',
                                   'bytes_in',
                                   'bytes_out',
                                   'duration',
                                   'packets_in',
                                   'packets_out',
                                   'resp_bytes',
                                   'tcp_flag',
                                   'transport',
                                   'tunnel_parents']

    def get_conn_info(self, iocsaw_dict):
        ips = iocsaw_dict.keys()
        conn_info = {}
        for ip in ips:
            earliest = iocsaw_dict[ip]['firstseen']
            latest = iocsaw_dict[ip]['lastseen']
            e = self._get_conn_info(earliest, ip)
            l = self._get_conn_info(latest, ip)
            conn_info[ip] = [json.loads(e.read()), json.loads(l.read())]
        return conn_info

    def _get_conn_info(self, around_time, ip, time_range=2):
        search_str = 'search earliest={earliest} latest={latest} (index=bro_conn OR index=bro_http OR index=bro_dns) "{ip}"'
        s = search_str.format(earliest=around_time-time_range,
                              latest=around_time+time_range,
                              ip=ip)
        response = self.splunk_service.jobs.oneshot(s,
                   output_mode='json',
                   field_list = ','.join(self.splunk_flow_fields))
        return response

    def _check_splunk_hashes(self, around_time, hash_list, time_range=5):
        search_str = 'search earliest={earliest} latest={latest} `hash_indexes` ({hashes})'
        hash_list = ['"{}"'.format(md5) for md5 in hash_list]
        s = search_str.format(earliest=around_time-time_range,
                              latest=around_time+time_range,
                              hashes=' OR '.join(hash_list))
        response = self.splunk_service.jobs.oneshot(s, output_mode='json')
        return response

    def check_splunk_hashes(self, iocsaw_dict, vt_file_reports):
        ips = [ip for ip in iocsaw_dict.keys() if ip in vt_file_reports]
        hash_hits = {}
        for ip in ips:
            earliest = iocsaw_dict[ip]['firstseen']
            latest = iocsaw_dict[ip]['lastseen']
            md5s = [f['md5'] for f in vt_file_reports[ip] if type(f) is dict]
            if len(md5s) > 0:
                e = self._check_splunk_hashes(earliest, md5s)
                l = self._check_splunk_hashes(latest, md5s)
                hash_hits[ip] = [json.loads(e.read()), json.loads(l.read())]
        return hash_hits

    def _vt_file_lookup(self, resource_list):
        '''resource can be scan_id, sha256, etc. up to 25 values'''
        url = 'https://www.virustotal.com/vtapi/v2/file/report'
        params={'resource' : ','.join(resource_list), 'apikey' : config.VT_API_KEY}
        r = requests.get(url, params=params)
        return json.loads(r.text)

    def get_vt_file_lookup(self, vt_ip_report):
        file_lookup = defaultdict(list)
        for ip in vt_ip_report.keys():
            vt_nested_fields = ['detected_communicating_samples',
                                'detected_downloaded_samples',
                                'detected_referrer_samples']
            hashes = set()
            for f in vt_nested_fields:
                if f in vt_ip_report[ip]:
                    hashes.update([x['sha256'] for x in vt_ip_report[ip][f]])
            hashes = list(hashes)
            for h in self.chunker(hashes, 25):
                file_lookup[ip] += self._vt_file_lookup(h)
        return file_lookup

    def chunker(self, seq, size):
        return(seq[pos:pos + size] for pos in xrange(0, len(seq), size))

    def get_sgraph_info(self, ips):
        sgraph_info = {}
        for ip in ips:
            sec_info = self.inv.get_security_info(ip)
            categorization = self.inv.get_categorization(ip)
            sec_info.update(categorization)
            sgraph_info[ip] = sec_info
        return sgraph_info

    def get_related_domains(self, ips):
        related_domains = {}
        for ip in ips:
            related_domains[ip] = {
                'latest_malicious_domains' : self.inv.get_latest_domains(ip),
                'rr_history_a' : self.inv.rr_history_ip(ip, query_type='A'),
                'rr_history_ns' : self.inv.rr_history_ip(ip, query_type='NS')}
        return related_domains

    def get_iocsaw_info(self, ips):
        seen = json.loads(self.scrypture.check_iocsaw(indicators=ips)['output'])
        seen_dict = {i['item']:i for i in seen}
        return seen_dict

    def get_wam(self, ips):
        blocked = json.loads(self.scrypture.wam_lookup(domains_and_ips=ips)['output'])
        blocked_dict = {i['ipaddress']:i for i in blocked}
        return blocked_dict

    def json_to_csv(self, json_input, headers=None):
        '''
        Convert simple JSON to CSV
        Accepts a JSON string or JSON object
        '''
        try:
            json_input = json.loads(json_input)
        except:
            pass # If loads fails, it's probably already parsed
        if headers is None:
            headers = set()
            for json_row in json_input:
                headers.update(json_row.keys())
        csv_io = StringIO.StringIO()
        csv_out = csv.DictWriter(csv_io,headers)
        csv_out.writeheader()
        for json_row in json_input:
            csv_out.writerow(json_row)
        csv_io.seek(0)
        return csv_io.read()

    def get_ip_whois(self, ips):
        whois = {}
        for ip in ips:
            try:
                whois[ip] = ipwhois.IPWhois(ip).lookup_rws()
            except:
                whois[ip] = {"error":"Error looking up whois info", "nets":[{}]}
        return whois

    def get_isight(self, ips):
        isight_reports = {}
        for ip in ips:
            status_code, text = isight.download('/search/basic', {'ip':ip})
            if status_code in [403, 429, 503]:
                print "Rate limit exceeded, sleeping..."
                time.sleep(11)
                status_code, text = isight.download('/search/basic', {'ip':ip})
            elif status_code == 200: #Found!
                isight_reports[ip] = json.loads(text)
            elif status_code != 204: #204 means no match, else error
                isight_reports[ip] = 'Error {}'.format(status_code)
        return isight_reports

    def get_vt_domain_report(self, domains):
        vt_info = {}
        if not isinstance(domain, list):
            domains = [domains]
        for domain in domains:
            url = 'https://www.virustotal.com/vtapi/v2/domain/report'
            params={'domain' : domain, 'apikey' : config.VT_API_KEY}
            r = requests.get(url, params=params)
            vt_info[domain] = json.loads(r.text)
        return vt_info

    def get_vt_ip_report(self, ips):
        vt_info = {}
        for ip in ips:
            url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
            params={'ip' : ip, 'apikey' : config.VT_API_KEY}
            r = requests.get(url, params=params)
            vt_info[ip] = json.loads(r.text)
        return vt_info

    def get_header_from_dict(self, d):
        headers = set()
        for k,v in d.items():
            headers.update(v.keys())
        return list(headers)

    def get_header(self, l):
        headers = set()
        for row in l:
            headers.update(row.keys())
        return list(headers)

    def process_ips(self, ips):
#        domains = [d for d in ips if not _is_ip(d)]
#        ips = [ip for ip in ips if ip not in domains]
#        ip_info['vt_domain'] = self.get_vt_domain_report(ip)

        ip_info = {}
        ### Get all the basic info we can get
        ip_info['sgraph'] = self.get_sgraph_info(ips)
        ip_info['wam'] = self.get_wam(ips)
        ip_info['iocsaw'] = self.get_iocsaw_info(ips)
        ip_info['vt_ip_report'] = self.get_vt_ip_report(ips)
        #ip_info['ip_whois'] = self.get_ip_whois(ips)
        ip_info['related_domains'] = self.get_related_domains(ips)
        ip_info['isight_search'] = self.get_isight(ips)

        ### Now go deeper...
        seen_ips = [ip for ip in ips if ip in ip_info['iocsaw']]
        ip_info['conn_info'] = self.get_conn_info(ip_info['iocsaw'])
        ip_info['vt_file_report'] = self.get_vt_file_lookup(
                                        ip_info['vt_ip_report'])

        ### Deeper still...
        ip_info['splunk_hash_search'] = self.check_splunk_hashes(
                                            ip_info['iocsaw'],
                                            ip_info['vt_file_report'])
#        all_domains = []
#        for ip,related in ip_info['related_domains'].items():
#            malicious = related['latest_malicious_domains']
#            rr_a = related['rr_history_a']
#            rr_ns = related['rr_history_ns']
#            all_domains += [str(d) for d in list(set(malicious+rr_a+rr_ns))]

#        ip_info['domain_sgraph'] = self.get_sgraph_info(all_domains)
        return ip_info

    def _is_ip(self, indicator):
        ip_format = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        return ip_format.match(indicator)


