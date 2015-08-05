"""
VirusTotal domain lookup
"""

import requests
from collections import defaultdict
import json
import config
import re
from dbcache import dbcache


def get_domain_report(domains, force_update=False):
    vt_info = []
    if not isinstance(domains, list):
        domains = [domains]
    for domain in domains:
        vt_info.append(_get_domain_report(domain, force_update=force_update))
    return vt_info

@dbcache
def _get_domain_report(domain, force_update=False):
    vt_info = {'indicator' : domain}
    url = 'https://www.virustotal.com/vtapi/v2/domain/report'
    params={'domain' : domain, 'apikey' : config.VT_API_KEY}
    r = requests.get(url, params=params, proxies=config.PROXIES)
    vt_info.update(json.loads(r.text))

    url = 'https://www.virustotal.com/vtapi/v2/url/report'
    params={'resource' : domain, 'apikey' : config.VT_API_KEY}
    r = requests.get(url, params=params, proxies=config.PROXIES)
    vt_info.update(json.loads(r.text))
    return vt_info

def _vt_file_lookup(resource_list):
    '''VirusTotal file lookup. Resource can be scan_id, sha256, etc.
    up to 25 values'''
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params={'resource' : ','.join(resource_list), 'apikey' : config.VT_API_KEY}
    r = requests.get(url, params=params, proxies=config.PROXIES)
    results = json.loads(r.text)
    if type(results) != list:
        results = [results]
    return results

@dbcache
def get_file_lookup(hashes):
    hashes = list(hashes)
    file_lookups = []
    for h in utils.chunker(hashes, 25):
        file_lookups += _vt_file_lookup(h)
    return file_lookups

def get_ip_report(ips, force_update=False):
    vt_info = []
    if not isinstance(ips, list):
        ips = [ips]
    for ip in ips:
        vt_info.append(_get_ip_report(ip, force_update=force_update))
    return vt_info

@dbcache
def _get_ip_report(ip, force_update=False):
    '''VirusTotal IP report'''
    vt_info = {'indicator' : ip}
    url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
    params={'ip' : ip, 'apikey' : config.VT_API_KEY}
    r = requests.get(url, params=params, proxies=config.PROXIES)
    vt_info.update(json.loads(r.text))

    url = 'https://www.virustotal.com/vtapi/v2/url/report'
    params={'resource' : ip, 'apikey' : config.VT_API_KEY}
    r = requests.get(url, params=params, proxies=config.PROXIES)
    vt_info.update(json.loads(r.text))
    return vt_info
